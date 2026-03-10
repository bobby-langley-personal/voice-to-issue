"""
FastAPI Voice-to-Issue Application
Converts voice recordings into GitHub issues using Claude AI
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import asyncio
import logging
from pathlib import Path

from voice_processor import VoiceProcessor
from issue_creator import IssueCreator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice-to-Issue",
    description="Convert voice recordings into GitHub issues using AI",
    version="1.0.0"
)

# Initialize components
voice_processor = VoiceProcessor()
issue_creator = IssueCreator()

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main voice recording interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-voice")
async def upload_voice(
    audio_file: UploadFile = File(...),
    repository: str = Form(...),
    context: str = Form(default="")
):
    """Process uploaded voice file and create GitHub issue"""
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read audio data
        audio_data = await audio_file.read()
        
        # Process voice to text
        text_content = await voice_processor.process_audio(audio_data, audio_file.content_type)
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from audio")
        
        # Create GitHub issue
        issue_data = await issue_creator.create_issue(
            repository=repository,
            voice_text=text_content,
            context=context
        )
        
        return JSONResponse({
            "success": True,
            "message": "Issue created successfully!",
            "issue_url": issue_data.get("html_url"),
            "issue_number": issue_data.get("number"),
            "transcription": text_content,
            "title": issue_data.get("title")
        })
        
    except Exception as e:
        logger.error(f"Error processing voice upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-issue")
async def text_to_issue(
    text_content: str = Form(...),
    repository: str = Form(...),
    context: str = Form(default="")
):
    """Create GitHub issue from text input (fallback for voice)"""
    try:
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        # Create GitHub issue
        issue_data = await issue_creator.create_issue(
            repository=repository,
            voice_text=text_content,
            context=context
        )
        
        return JSONResponse({
            "success": True,
            "message": "Issue created successfully!",
            "issue_url": issue_data.get("html_url"),
            "issue_number": issue_data.get("number"),
            "title": issue_data.get("title")
        })
        
    except Exception as e:
        logger.error(f"Error creating issue from text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "voice-to-issue"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
