import httpx
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi import Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, Optional, Any
from comfy_sdk import Comfy
from fastapi.staticfiles import StaticFiles
import uuid
from pathlib import Path
import json
import shutil
from sqlalchemy.orm import Session
from database import get_db, Character
import os
from dotenv import load_dotenv

app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# Ensure directories exist BEFORE mounting StaticFiles
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
input_dir = Path("inputs")
input_dir.mkdir(exist_ok=True)

app.mount("/outputs", StaticFiles(directory="outputs"), name="present outputs")

jobs = {}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "https://tingyuruanrty.github.io",
    "http://127.0.0.1:5500/index.html"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load .env file directly in Python (handles Windows CRLF properly)
load_dotenv(override=True)

# Strip whitespace AND any accidental quotes around the key
NEW_KEY = os.getenv("COMFY_CLOUD_API_KEY", "").strip().strip('"').strip("'")
client = Comfy(api_key=NEW_KEY)

# FIX: Force get_job to use the job ID instead of the full urls.self URL
# so comfy_low never strips the Authorization: Bearer header when polling!
_orig_get_job = client._low.get_job
client._low.get_job = lambda job_or_url, *a, **kw: _orig_get_job(
    job_or_url.rstrip("/").split("/")[-1], *a, **kw
)

@app.get("/")
async def root():
    return {"status": "online", "message": "Server is up and running"}


@app.get("/api/characters")
async def list_characters(db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    character_list = [
        {
            "id": char.id,
            "name": char.name,
            "trigger_word": char.trigger_word,
            "lora_filename": char.lora_filename
        }
        for char in characters
    ]
    return {
        "status": "good",
        "characters": character_list,
        "message": "Job successfully finished",
    }


def upload_asset(upload_file: UploadFile) -> Any:
    # 1. Extract file extension (e.g. ".png", ".gif")
    extension = Path(upload_file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{extension}"
    save_path = input_dir / unique_filename

    # 2. Write the incoming stream to disk
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # 3. Push to Comfy Cloud assets (returns an Asset handle used by wf.set_input)
    cloud_asset = client.assets.from_file(str(save_path))
    return cloud_asset


def run_generation(
    job_id: str,
    prompt: str,
    negative_prompt: Optional[str],
    character_asset: Optional[Any],
    lora_filename: Optional[str],
    motion_asset: Optional[Any]
):
    try:
        # Load the new AnimateDiff workflow JSON
        wf = client.workflows.from_file("animatediffusion.json")
        
        # Node 3: Positive prompt
        wf.set_input("3", "text", prompt)
        
        # Node 57: Character reference image (LoadImage)
        if character_asset:
            wf.set_input("57", "image", character_asset)
            
        # Node 12: LoRA Loader
        if lora_filename:
            wf.set_input("12", "lora_name", lora_filename)
            
        # Node 22: Negative prompt
        if negative_prompt:
            wf.set_input("22", "text", negative_prompt)
            
        # Node 96: Motion GIF reference (LoadImage node in animatediffusion.json)
        if motion_asset:
            wf.set_input("96", "image", motion_asset)

        # Blocking generation happens here in the background thread
        job = client.run(wf)
        
        # Node 9: SaveImage (individual frames)
        outputs = job.get_outputs("9")

        saved_files = []
        for output in outputs:
            unique_filename = f"{uuid.uuid4()}_{output.name}"
            save_path = output_dir / unique_filename
            output.to_file(str(save_path))
            # .as_posix() ensures forward slashes (outputs/...) on both Windows and Linux
            saved_files.append(f"https://dwybuisa1bwwg.cloudfront.net/{save_path.as_posix()}")

        # Update the job state to completed
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["image_urls"] = saved_files

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Job {job_id} failed with error: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/api/generate")
def create_sprite_job(
    background_tasks: BackgroundTasks,
    prompt: Annotated[str, Form()],
    negative_prompt: Annotated[Optional[str], Form()] = None,
    character_image: Annotated[Optional[UploadFile], File()] = None,
    lora_filename: Annotated[Optional[str], Form()] = None,
    motion_video: Annotated[Optional[UploadFile], File()] = None
):
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    job_id = str(uuid.uuid4())

    # Upload files to Comfy Cloud assets before returning the response
    character_asset = upload_asset(character_image) if character_image else None
    motion_asset = upload_asset(motion_video) if motion_video else None

    # Register initial job status
    jobs[job_id] = {
        "status": "processing",
        "image_urls": [],
        "error": None
    }

    # Queue the heavy generation to run in the background
    background_tasks.add_task(
        run_generation,
        job_id=job_id,
        prompt=prompt,
        negative_prompt=negative_prompt,
        character_asset=character_asset,
        lora_filename=lora_filename,
        motion_asset=motion_asset
    )

    # Return immediately to the client
    return {
        "status": "queued",
        "job_id": job_id,
        "message": "Job received and processing in background"
    }


@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job