from __future__ import annotations

import os
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sprite_jobs.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ------------------------------------------------------------
# Database model
# ------------------------------------------------------------
class SpriteJob(Base):
    __tablename__ = "sprite_jobs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    character_name = Column(String(255), nullable=True)
    status = Column(String(50), default="queued", nullable=False)
    comfy_workflow_name = Column(String(255), default="character_motion_v1", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    result_url = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# Request / response models
# ------------------------------------------------------------
class JobCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Text prompt describing the animation request")
    character_name: str | None = Field(default=None, description="Character name or identifier")
    reference_video_url: str | None = Field(default=None, description="Optional reference GIF/video URL")
    style: str = Field(default="anime", description="Art style or look to use")
    frame_count: int = Field(default=8, ge=1, le=40, description="Total frames to generate")


class JobResponse(BaseModel):
    job_id: int
    status: str
    prompt: str
    message: str


# ------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------
app = FastAPI(
    title="AI Sprite Generator API",
    description="Backend service for queuing sprite generation jobs and interacting with Comfy Cloud.",
    version="1.0.0",
)


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is the place where you later call Comfy Cloud's API.
# For now it is just a placeholder so the project structure is easy to extend.
async def call_comfy_cloud_api(job: SpriteJob) -> None:
    """Send a generated workflow payload to Comfy Cloud and update the job when it finishes."""
    # Example idea:
    # - load workflow JSON
    # - modify nodes with prompt + reference URL
    # - send POST request to Comfy Cloud
    # - save output image URLs or frame URLs
    # - update job.status = "completed"
    # This function will be expanded later.
    return None


# ------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------
@app.get("/")
def check_health():
    return {
        "status": "online",
        "message": "Server is up and running",
        "database": DATABASE_URL,
    }


@app.post("/generate", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def create_sprite_job(payload: JobCreateRequest):
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    db = SessionLocal()
    job = SpriteJob(
        prompt=payload.prompt.strip(),
        character_name=payload.character_name,
        status="queued",
        comfy_workflow_name="character_motion_v1",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()

    return JobResponse(
        job_id=job.id,
        status="queued",
        prompt=job.prompt,
        message="Job successfully queued. Comfy Cloud processing can be connected here.",
    )


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    db = SessionLocal()
    job = db.query(SpriteJob).filter(SpriteJob.id == job_id).first()
    db.close()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.id,
        status=job.status,
        prompt=job.prompt,
        message="Job retrieved successfully",
    )


# ------------------------------------------------------------
# Optional test route for frontend communication
# ------------------------------------------------------------
@app.get("/ping")
def ping():
    return {"message": "API is reachable"}
