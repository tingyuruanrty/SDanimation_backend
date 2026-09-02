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
client = Comfy(api_key="Comfyui-0ee5f666922fe5a361e43bc743d6c55d663ad0f38d68cf13b73b9ef89ce6d90a")


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
  
  # alter the workflow json file based on the request parameters here, tomorrow's work
  
  
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