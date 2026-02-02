from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path

from .database import get_db, init_db
from . import models, schemas
from .services.video_downloader import VideoDownloader
from .services.gemini_service import GeminiService
from .services.store_scraper import StoreScraper
from .services.export_service import ExportService

# Initialize FastAPI app
app = FastAPI(
    title="Recipe Extractor API",
    description="Extract cooking recipes from TikTok and Instagram videos using Google Gemini 3 Pro with advanced reasoning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
Path("data/images").mkdir(parents=True, exist_ok=True)
Path("data/exports").mkdir(parents=True, exist_ok=True)
Path("data/videos").mkdir(parents=True, exist_ok=True)
app.mount("/images", StaticFiles(directory="data/images"), name="images")
app.mount("/exports", StaticFiles(directory="data/exports"), name="exports")
app.mount("/videos", StaticFiles(directory="data/videos"), name="videos")

# Initialize services (GeminiService will be created per request with selected model)
video_downloader = VideoDownloader()
store_scraper = StoreScraper()
export_service = ExportService()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Recipe Extractor API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/api/recipes/extract", response_model=schemas.RecipeResponse)
async def extract_recipe(
    recipe_input: schemas.RecipeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Extract recipe from TikTok or Instagram video URL
    """
    try:
        video_url = recipe_input.video_url
        selected_model = recipe_input.model or "gemini-3-flash-preview"

        # Check if recipe already exists
        existing_recipe = db.query(models.Recipe).filter(
            models.Recipe.video_url == video_url
        ).first()

        if existing_recipe:
            return schemas.RecipeResponse(
                success=True,
                message="Recipe already exists in database",
                recipe=existing_recipe
            )

        # Download video
        platform, video_path, thumbnail_path = video_downloader.download_video(video_url)

        # Create GeminiService with selected model
        gemini_service = GeminiService(model_name=selected_model)

        # Analyze video with Gemini
        recipe_data = gemini_service.analyze_video(video_path)

        # Create recipe in database
        db_recipe = models.Recipe(
            title=recipe_data.get('title'),
            video_url=video_url,
            platform=platform,
            thumbnail_path=thumbnail_path,
            video_path=video_path,
            description=recipe_data.get('description')
        )
        db.add(db_recipe)
        db.flush()

        # Add ingredients
        for ing_data in recipe_data.get('ingredients', []):
            # Get store links for each ingredient
            store_links = store_scraper.find_ingredient_stores(ing_data['name'])

            ingredient = models.Ingredient(
                recipe_id=db_recipe.id,
                name=ing_data['name'],
                quantity=ing_data.get('quantity'),
                unit=ing_data.get('unit'),
                store_links=store_links
            )
            db.add(ingredient)

        # Add cooking steps
        for step_data in recipe_data.get('steps', []):
            step = models.CookingStep(
                recipe_id=db_recipe.id,
                step_number=step_data['step_number'],
                instruction=step_data['instruction'],
                duration=step_data.get('duration')
            )
            db.add(step)

        # Add nutrition info
        nutrition_data = recipe_data.get('nutrition', {})
        if nutrition_data and any(nutrition_data.values()):
            nutrition = models.NutritionInfo(
                recipe_id=db_recipe.id,
                calories=nutrition_data.get('calories'),
                protein=nutrition_data.get('protein'),
                carbs=nutrition_data.get('carbs'),
                fats=nutrition_data.get('fats'),
                fiber=nutrition_data.get('fiber'),
                servings=nutrition_data.get('servings')
            )
            db.add(nutrition)

        db.commit()
        db.refresh(db_recipe)

        return schemas.RecipeResponse(
            success=True,
            message="Recipe extracted successfully",
            recipe=db_recipe
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recipes", response_model=List[schemas.Recipe])
async def get_recipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all recipes"""
    recipes = db.query(models.Recipe).offset(skip).limit(limit).all()
    return recipes


@app.get("/api/recipes/{recipe_id}", response_model=schemas.Recipe)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.delete("/api/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"success": True, "message": "Recipe deleted successfully"}


@app.get("/api/recipes/{recipe_id}/grocery-list")
async def get_grocery_list(recipe_id: int, db: Session = Depends(get_db)):
    """Get grocery list for a recipe"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredients_data = [
        {
            "name": ing.name,
            "quantity": ing.quantity,
            "unit": ing.unit
        }
        for ing in recipe.ingredients
    ]

    shopping_list = store_scraper.create_shopping_list(ingredients_data)

    return {
        "recipe_id": recipe.id,
        "recipe_title": recipe.title,
        "shopping_list": shopping_list
    }


@app.get("/api/recipes/{recipe_id}/export/json")
async def export_recipe_json(recipe_id: int, db: Session = Depends(get_db)):
    """Export recipe to JSON"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "video_url": recipe.video_url,
        "platform": recipe.platform,
        "thumbnail_path": recipe.thumbnail_path,
        "ingredients": [
            {
                "name": ing.name,
                "quantity": ing.quantity,
                "unit": ing.unit,
                "store_links": ing.store_links
            }
            for ing in recipe.ingredients
        ],
        "steps": [
            {
                "step_number": step.step_number,
                "instruction": step.instruction,
                "duration": step.duration
            }
            for step in sorted(recipe.steps, key=lambda x: x.step_number)
        ],
        "nutrition": {
            "calories": recipe.nutrition.calories if recipe.nutrition else None,
            "protein": recipe.nutrition.protein if recipe.nutrition else None,
            "carbs": recipe.nutrition.carbs if recipe.nutrition else None,
            "fats": recipe.nutrition.fats if recipe.nutrition else None,
            "fiber": recipe.nutrition.fiber if recipe.nutrition else None,
            "servings": recipe.nutrition.servings if recipe.nutrition else None,
        } if recipe.nutrition else None
    }

    filepath = export_service.export_to_json(recipe_data, recipe_id)
    return FileResponse(filepath, media_type="application/json", filename=f"recipe_{recipe_id}.json")


@app.get("/api/recipes/{recipe_id}/export/pdf")
async def export_recipe_pdf(recipe_id: int, db: Session = Depends(get_db)):
    """Export recipe to PDF"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "description": recipe.description,
        "video_url": recipe.video_url,
        "thumbnail_path": recipe.thumbnail_path,
        "ingredients": [
            {
                "name": ing.name,
                "quantity": ing.quantity,
                "unit": ing.unit
            }
            for ing in recipe.ingredients
        ],
        "steps": [
            {
                "step_number": step.step_number,
                "instruction": step.instruction,
                "duration": step.duration
            }
            for step in sorted(recipe.steps, key=lambda x: x.step_number)
        ],
        "nutrition": {
            "calories": recipe.nutrition.calories if recipe.nutrition else None,
            "protein": recipe.nutrition.protein if recipe.nutrition else None,
            "carbs": recipe.nutrition.carbs if recipe.nutrition else None,
            "fats": recipe.nutrition.fats if recipe.nutrition else None,
            "fiber": recipe.nutrition.fiber if recipe.nutrition else None,
            "servings": recipe.nutrition.servings if recipe.nutrition else None,
        } if recipe.nutrition else None
    }

    filepath = export_service.export_to_pdf(recipe_data, recipe_id)
    return FileResponse(filepath, media_type="application/pdf", filename=f"recipe_{recipe_id}.pdf")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Recipe Extractor API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
