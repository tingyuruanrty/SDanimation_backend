import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, Optional
from comfy_sdk import Comfy
from fastapi.staticfiles import StaticFiles
import uuid
from pathlib import Path
import json
import shutil
from sqlalchemy.orm import Session
from database import get_db, Character
# my backend should receive a request body from browser, send back a response body

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# static file
# https://fastapi.tiangolo.com/tutorial/static-files/
# add a image view in the path /outputs
app.mount("/outputs", StaticFiles(directory="outputs"), name="present outputs")

# Create the outputs directory if it does not exist
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
input_dir = Path("inputs")
input_dir.mkdir(exist_ok=True)

def upload_asset(upload_file: UploadFile) -> str:
  # 1. Extract file extension (e.g. ".png", ".gif")
  extension = Path(upload_file.filename).suffix
  unique_filename = f"{uuid.uuid4()}{extension}"
  save_path = input_dir / unique_filename

  # 2. Write the incoming stream to disk
  with open(save_path, "wb") as buffer:
    shutil.copyfileobj(upload_file.file, buffer)

  # 3. Push to Comfy Cloud assets
  cloud_asset = client.assets.from_file(str(save_path))

  # Optional: Delete from your disk immediately if you don't want to hoard user uploads
  # save_path.unlink()
  
  ans = str(cloud_asset.id)
  if ans.endswith(extension):
    return ans
  return f"{ans}{extension}"


# list of allowed origins for cors
# frontend with these origins can access the backend
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Connect to comfy cloud api with api key
# man, i'm totally walking on the street without pants
NEW_KEY = "comfyui-a12b3c56ce23d2195663501692976c09c88de645b3ef9885250698bc379c2f5c".strip()

client = Comfy(api_key=NEW_KEY)


# path operation decorator
# when receive a http request of get operation on the root path, the function below will handel it
@app.get("/")
# path operation function, it will get called
async def root():
  return {"status": "online", "message": "Server is up and running"}

# 9/11/2026 work on this
# a list of character objects should be included in the response body, the key should be characters
# by convention, get don't alter resources at the backend
@app.get("/api/characters")
async def list_characters(db: Session = Depends(get_db)):
# Query all characters from the table
  characters = db.query(Character).all()

  # Map the database objects into regular Python dictionaries
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

# Main generation endpoint (POST request)
# need to parse the request body to get all the parameters for the sprite generation
# we are receiving a FormData object as the request body

# i need to change something here
@app.post("/api/generate")
def create_sprite_job(
  prompt: Annotated[str, Form()], 
  negative_prompt: Annotated[Optional[str], Form()] = None,
  character_image: Annotated[Optional[UploadFile], File()] = None,
  lora_filename: Annotated[Optional[str], Form()] = None,
  motion_video: Annotated[Optional[UploadFile], File()] = None
  ):
  
  # Data validation check
  if not prompt.strip():
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")
  
  with open("baseWorkflowChangeOnTopOfThis.json", "r", encoding="utf-8") as f:
    wf_data = json.load(f)
    
  wf_data["3"]["inputs"]["text"] = prompt
  
  if negative_prompt and negative_prompt.strip():
    wf_data["22"]["inputs"]["text"] = negative_prompt

  if character_image:
    wf_data["57"]["inputs"]["image"] = upload_asset(character_image)

  if lora_filename:
    wf_data["12"]["inputs"]["lora_name"] = lora_filename

  if motion_video:
    wf_data["60"]["inputs"]["video"] = upload_asset(motion_video)
  
  # call comfy cloud api to generate the sprite sheet
  wf = client.workflows.from_json(wf_data)
  # wf = await client.workflows.from_file("baseWorkflowChangeOnTopOfThis.json")
  
  job = client.run(wf)
  # out put pictures from the comfy cloud is in outputs now, i will need to save it on the disk, and send back the url to front end.
  outputs =  job.get_outputs("9")
  
  saved_files = []
  for output in outputs:
    # put uuid in the front so that there's never repeat name for file
    unique_filename = f"{uuid.uuid4()}_{output.name}"
    save_path = str( output_dir / unique_filename)
    output.to_file(save_path)
    saved_files.append(f"http://127.0.0.1:8000/{save_path}")

  # Return a temporary structured response for testing
  return {
      "status": "good",
      "image_urls": saved_files,
      "message": "Job successfully finished",
  }