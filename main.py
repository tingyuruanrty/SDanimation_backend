import httpx
from fastapi import FastAPI, HTTPException

# Initialize the main application object
app = FastAPI(
    title="AI Sprite Generator API",
    description="Backend service for handling sprite generation requests.",
    version="1.0.0",
)


# Health check endpoint (GET request)
@app.get("/")
def check_health():
  return {"status": "online", "message": "Server is up and running"}


# Main generation endpoint (POST request)
@app.post("/generate")
def create_sprite_job(prompt: str):
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