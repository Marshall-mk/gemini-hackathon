"""
Modal deployment configuration for Recipe Extractor backend.
This file deploys the FastAPI app to Modal's serverless platform.
"""

import modal
from pathlib import Path

# Create Modal app
app = modal.App("recipe-extractor")

# Create image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi==0.109.0",
        "uvicorn[standard]==0.25.0",
        "sqlalchemy==2.0.25",
        "pydantic==2.5.3",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "yt-dlp==2024.1.1",
        "instaloader==4.10",
        "opencv-python-headless==4.9.0.80",  # headless version for serverless
        "google-generativeai==0.3.2",
        "reportlab==4.0.9",
        "Pillow==10.2.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.3",
        "aiofiles==23.2.1",
    )
    .apt_install("ffmpeg")  # Required for video processing
)

# Create persistent volumes for temporary storage
videos_volume = modal.Volume.from_name("recipe-videos", create_if_missing=True)
images_volume = modal.Volume.from_name("recipe-images", create_if_missing=True)
exports_volume = modal.Volume.from_name("recipe-exports", create_if_missing=True)

# Mount the app code
mounts = [
    modal.Mount.from_local_dir(
        Path(__file__).parent / "app",
        remote_path="/root/app"
    )
]


@app.function(
    image=image,
    mounts=mounts,
    secrets=[modal.Secret.from_name("gemini-api-key")],
    volumes={
        "/root/data/videos": videos_volume,
        "/root/data/images": images_volume,
        "/root/data/exports": exports_volume,
    },
    timeout=600,  # 10 minutes for video processing
    allow_concurrent_inputs=10,
    container_idle_timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    """
    Deploy FastAPI application to Modal.
    """
    import os
    from app.main import app as fastapi_app
    from app.database import init_db

    # Initialize database on startup
    init_db()

    return fastapi_app


# Local testing
if __name__ == "__main__":
    # For local development, run: modal serve modal_app.py
    # For deployment, run: modal deploy modal_app.py
    pass
