from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import shutil
import asyncio
import random
from api_runway import router as runway_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()
app.include_router(runway_router, prefix="/api/runway")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Create uploads directory
uploads_dir = ROOT_DIR / "uploads"
uploads_dir.mkdir(exist_ok=True)

# Models
class VideoGenerationRequest(BaseModel):
    prompt: str
    style: str  # realistic, anime, cartoon, surreal, talking_image
    duration: int = Field(default=7, ge=5, le=10)
    nsfw_enabled: bool = Field(default=False)

class ImageToVideoRequest(BaseModel):
    style: str  # character_animation, movement_overlay, talking_face
    duration: int = Field(default=7, ge=5, le=10)
    nsfw_enabled: bool = Field(default=False)

class VideoResponse(BaseModel):
    id: str
    prompt: Optional[str] = None
    image_filename: Optional[str] = None
    style: str
    duration: int
    status: str  # generating, completed, failed
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    nsfw_enabled: bool = Field(default=False)

class UserGallery(BaseModel):
    videos: List[VideoResponse]
    total_count: int

# Sample video URLs and thumbnails for different styles
SAMPLE_VIDEOS = {
    "realistic": [
        {
            "video_url": "https://images.pexels.com/photos/11262264/pexels-photo-11262264.jpeg",
            "thumbnail_url": "https://images.pexels.com/photos/11262264/pexels-photo-11262264.jpeg"
        },
        {
            "video_url": "https://images.pexels.com/photos/7480538/pexels-photo-7480538.jpeg",
            "thumbnail_url": "https://images.pexels.com/photos/7480538/pexels-photo-7480538.jpeg"
        }
    ],
    "anime": [
        {
            "video_url": "https://images.pexels.com/photos/18069362/pexels-photo-18069362.png",
            "thumbnail_url": "https://images.pexels.com/photos/18069362/pexels-photo-18069362.png"
        }
    ],
    "cartoon": [
        {
            "video_url": "https://images.unsplash.com/photo-1733590555923-2aa0e489300e",
            "thumbnail_url": "https://images.unsplash.com/photo-1733590555923-2aa0e489300e"
        }
    ],
    "surreal": [
        {
            "video_url": "https://images.pexels.com/photos/24182512/pexels-photo-24182512.jpeg",
            "thumbnail_url": "https://images.pexels.com/photos/24182512/pexels-photo-24182512.jpeg"
        }
    ],
    "talking_image": [
        {
            "video_url": "https://images.unsplash.com/photo-1717632464005-1f33909e484b",
            "thumbnail_url": "https://images.unsplash.com/photo-1717632464005-1f33909e484b"
        }
    ],
    "character_animation": [
        {
            "video_url": "https://images.pexels.com/photos/17722043/pexels-photo-17722043.jpeg",
            "thumbnail_url": "https://images.pexels.com/photos/17722043/pexels-photo-17722043.jpeg"
        }
    ],
    "movement_overlay": [
        {
            "video_url": "https://images.pexels.com/photos/32539017/pexels-photo-32539017.jpeg",
            "thumbnail_url": "https://images.pexels.com/photos/32539017/pexels-photo-32539017.jpeg"
        }
    ],
    "talking_face": [
        {
            "video_url": "https://images.unsplash.com/photo-1483478550801-ceba5fe50e8e",
            "thumbnail_url": "https://images.unsplash.com/photo-1483478550801-ceba5fe50e8e"
        }
    ]
}

async def simulate_video_generation(video_id: str, style: str):
    """Simulate video generation process"""
    await asyncio.sleep(3)  # Simulate processing time
    
    # Update video status to completed with sample content
    sample_content = random.choice(SAMPLE_VIDEOS.get(style, SAMPLE_VIDEOS["realistic"]))
    
    await db.videos.update_one(
        {"id": video_id},
        {
            "$set": {
                "status": "completed",
                "video_url": sample_content["video_url"],
                "thumbnail_url": sample_content["thumbnail_url"]
            }
        }
    )

@api_router.post("/generate-text-to-video", response_model=VideoResponse)
async def generate_text_to_video(request: VideoGenerationRequest):
    """Generate video from text prompt"""
    video_id = str(uuid.uuid4())
    
    video_data = {
        "id": video_id,
        "prompt": request.prompt,
        "style": request.style,
        "duration": request.duration,
        "status": "generating",
        "created_at": datetime.utcnow(),
        "nsfw_enabled": request.nsfw_enabled
    }
    
    # Save to database
    await db.videos.insert_one(video_data)
    
    # Start background video generation
    asyncio.create_task(simulate_video_generation(video_id, request.style))
    
    return VideoResponse(**video_data)

@api_router.post("/generate-image-to-video")
async def generate_image_to_video(
    file: UploadFile = File(...),
    style: str = Form(...),
    duration: int = Form(7),
    nsfw_enabled: bool = Form(False)
):
    """Generate video from uploaded image"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    video_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"{video_id}.{file_extension}"
    file_path = uploads_dir / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    video_data = {
        "id": video_id,
        "image_filename": filename,
        "style": style,
        "duration": duration,
        "status": "generating",
        "created_at": datetime.utcnow(),
        "nsfw_enabled": nsfw_enabled
    }
    
    # Save to database
    await db.videos.insert_one(video_data)
    
    # Start background video generation
    asyncio.create_task(simulate_video_generation(video_id, style))
    
    return VideoResponse(**video_data)

@api_router.get("/video/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """Get video by ID"""
    video = await db.videos.find_one({"id": video_id})
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return VideoResponse(**video)

@api_router.get("/videos", response_model=UserGallery)
async def get_user_videos(limit: int = 20, offset: int = 0):
    """Get user's video gallery"""
    videos = await db.videos.find().skip(offset).limit(limit).sort("created_at", -1).to_list(limit)
    total_count = await db.videos.count_documents({})
    
    video_responses = [VideoResponse(**video) for video in videos]
    
    return UserGallery(videos=video_responses, total_count=total_count)

@api_router.get("/styles")
async def get_available_styles():
    """Get available video styles"""
    return {
        "text_to_video_styles": [
            {"id": "realistic", "name": "Realistic", "description": "Photorealistic video generation"},
            {"id": "anime", "name": "Anime", "description": "Japanese animation style"},
            {"id": "cartoon", "name": "Cartoon", "description": "Western cartoon style"},
            {"id": "surreal", "name": "Surreal", "description": "Abstract and artistic style"},
            {"id": "talking_image", "name": "Talking Image", "description": "Face animation from image"}
        ],
        "image_to_video_styles": [
            {"id": "character_animation", "name": "Character Animation", "description": "Animate characters in the image"},
            {"id": "movement_overlay", "name": "Movement Overlay", "description": "Add dynamic movement effects"},
            {"id": "talking_face", "name": "Talking Face", "description": "Make faces speak and move"}
        ]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
