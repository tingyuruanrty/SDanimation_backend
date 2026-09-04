import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, Optional
from comfy_sdk import Comfy
from fastapi.staticfiles import StaticFiles
import uuid
from pathlib import Path
import json
# my backend should receive a request body from browser, send back a response body

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# add a image view in the path /outputs
app.mount("/outputs", StaticFiles(directory="outputs"), name="present outputs")

# Create the outputs directory if it does not exist
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

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

NEW_KEY = "comfyui-a12b3c56ce23d2195663501692976c09c88de645b3ef9885250698bc379c2f5c".strip()

client = Comfy(api_key=NEW_KEY)


# path operation decorator
# when receive a http request of get operation on the root path, the function below will handel it
@app.get("/")
# path operation function, it will get called
async def root():
  return {"status": "online", "message": "Server is up and running"}

# Main generation endpoint (POST request)
# need to parse the request body to get all the parameters for the sprite generation
# we are receiving a FormData object as the request body
@app.post("/api/generate")
def create_sprite_job(
  prompt: Annotated[str, Form()], 
  negative_prompt: Annotated[Optional[str], Form()] = None,
  character_image: Annotated[Optional[UploadFile], File()] = None,
  lora_file: Annotated[Optional[UploadFile], File()] = None,
  motion_video: Annotated[Optional[UploadFile], File()] = None
  ):
  
  # Data validation check
  if not prompt.strip():
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")
  
  # with open("baseWorkflowChangeOnTopOfThis.json", "r", encoding="utf-8") as f:
  #   wf_data = json.load(f)
    
  # wf_data["3"]["inputs"]["text"] = prompt
  
  # if negative_prompt and negative_prompt.strip():
  #   wf_data["22"]["inputs"]["text"] = negative_prompt

  # if character_image:
  

  
  # upload files are in parameters already, i should create a data base, add a row for each job, with all the parameters downloaded on the disk
  # because the client.assets.from_file() expect a file path

  
  #   uploaded_image = client.assets.from_file("path/to/my_input.png")
  #   wf_data["57"]["inputs"]["image"] = uploaded_image.name

  # if lora_file:
  #   wf_data["12"]["inputs"]["lora_name"] = upload_temp_asset(lora_file)

  # if motion_video:
  #   wf_data["60"]["inputs"]["video"] = upload_temp_asset(motion_video)
  
  # wf = client.workflows.from_dict(wf_data)
  
  
  # call comfy cloud api to generate the sprite sheet
  wf = client.workflows.from_file("baseWorkflowChangeOnTopOfThis.json")
  job = client.run(wf)
  # out put pictures from the comfy cloud is in outputs now, i will need to save it on the disk, and send back the url to front end.
  outputs = job.get_outputs("9")
  
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