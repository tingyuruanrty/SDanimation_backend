import httpx
from fastapi import FastAPI, HTTPException

# Initialize the main application object
# the parameters are used for automatically generating API documentation
app = FastAPI(
    title="Sprite Sheet Generator on comfycloud",
    description="Backend script for handling sprite generation requests.",
    version="1.0.0",
)

# path operation decorator
# when receive a http request of get operation on the root path, the function below will handel it
@app.get("/")
# path operation function, it will get called
async def root():
  return {"status": "online", "message": "Server is up and running"}


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