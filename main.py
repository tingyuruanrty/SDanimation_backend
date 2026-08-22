import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# list of allowed origins for cors
# frontend with these resources can access the backend
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post("/generate")
async def create_sprite_job(prompt: str):
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