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

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)
# static file
# https://fastapi.tiangolo.com/tutorial/static-files/
# "Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
app.mount("/outputs", StaticFiles(directory="outputs"), name="present outputs")

# Create the outputs directory if it does not exist
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
input_dir = Path("inputs")
input_dir.mkdir(exist_ok=True)

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
  
  return cloud_asset

# Main generation endpoint (POST request)
# need to parse the request body to get all the parameters for the sprite generation
# we are receiving a FormData object as the request body
@app.post("/api/generate")
def create_sprite_job(
  prompt: Annotated[str, Form()], 
  negative_prompt: Annotated[Optional[str], Form()] = None,
  character_image: Annotated[Optional[UploadFile], File()] = None,
  lora_filename: Annotated[Optional[str], Form()] = None,
  motion_video: Annotated[Optional[UploadFile], File()] = None
  ):

  # prompt is empty
  if not prompt.strip():
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")
  
  # https://docs.comfy.org/development/api-development/sdks
  wf = client.workflows.from_file("baseWorkflowChangeOnTopOfThis.json")
  wf.set_input("3", "text", prompt)
  if character_image:
    wf.set_input("57", "image", upload_asset(character_image))
  if lora_filename:
    wf.set_input("12", "lora_name", lora_filename)
  if negative_prompt:
    wf.set_input("22", "text", negative_prompt)
  if motion_video:
    wf.set_input("60", "video", upload_asset(motion_video))
  
  job = client.run(wf)
  # out put pictures from the comfy cloud is in outputs now, i will need to save it on the disk, and send back the url to front end.
  outputs = job.get_outputs("9")
  
  saved_files = []
  for output in outputs:
    # put uuid in the front so that there's never repeat name for file
    unique_filename = f"{uuid.uuid4()}_{output.name}"
    save_path = str(output_dir / unique_filename)
    output.to_file(save_path)
    saved_files.append(f"http://127.0.0.1:8000/{save_path}")

  # Return a temporary structured response for testing
  return {
      "status": "good",
      "image_urls": saved_files,
      "message": "Job successfully finished",
  }