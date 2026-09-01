import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from comfy_sdk import Comfy

# my backend should receive a request body from browser, send back a response body

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# list of allowed origins for cors
# frontend with these origins can access the backend
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = Comfy(api_key="Comfyui-0ee5f666922fe5a361e43bc743d6c55d663ad0f38d68cf13b73b9ef89ce6d90a")

# path operation decorator
# when receive a http request of get operation on the root path, the function below will handel it
@app.get("/")
# path operation function, it will get called
async def root():
  return {"status": "online", "message": "Server is up and running"}

@app.get("/{job_id}")
async def get_job_id(job_id: int):
  return {"job_id": job_id}

# Main generation endpoint (POST request)
# need to parse the request body to get all the parameters for the sprite generation
# we are receiving a FormData object as the request body
@app.post("/api/generate")
async def create_sprite_job(
  prompt: Annotated[str, Form()], 
  negative_prompt: Annotated[Optional[str], Form()] = None,
  character_image: Annotated[Optional[UploadFile], File()] = None,
  lora_file: Annotated[Optional[UploadFile], File()] = None,
  motion_video: Annotated[Optional[UploadFile], File()] = None):
  
  # call comfy cloud api to generate the sprite sheet
  # work on this tomorrow
  workflow = client.workflows.from_file("baseWorkflowChangeOnTopOfThis.json")
  job = client.run(workflow)
  outputs = job.get_outputs("62")
  # output_urls = [out.url for out in outputs]
  
  # Data validation check
  if not prompt.strip():
    raise HTTPException(status_code=400, detail="Prompt cannot be empty")

  # Return a temporary structured response for testing
  return {
      "status": "pending",
      "job_id": 101,
      "user_prompt": prompt,
      "message": "Job successfully queued",
  }