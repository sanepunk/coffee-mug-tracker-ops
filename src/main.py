from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import aiofiles
import uuid
from utils.tracking import CupTracker

app = FastAPI(title="Cup Detection API")

# Create directories for uploads and processed videos
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("static/processed")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process-video")
async def process_video(video: UploadFile = File(...)):
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())
    input_path = UPLOAD_DIR / f"{unique_id}_{video.filename}"
    
    try:
        # Save uploaded file
        async with aiofiles.open(input_path, 'wb') as f:
            content = await video.read()
            await f.write(content)
        
        # Process video
        tracker = CupTracker()
        output_path = OUTPUT_DIR / f"processed_{unique_id}_{video.filename}"
        processed_path = tracker.process_video(str(input_path))
        
        # Return processed video path
        return {"status": "success", "video_path": f"/static/processed/{output_path.name}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup input file
        if input_path.exists():
            input_path.unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
