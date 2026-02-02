from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime


class IngredientBase(BaseModel):
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    store_links: Optional[List[Dict[str, str]]] = None


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class CookingStepBase(BaseModel):
    step_number: int
    instruction: str
    duration: Optional[str] = None


class CookingStepCreate(CookingStepBase):
    pass


class CookingStep(CookingStepBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class NutritionInfoBase(BaseModel):
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    servings: Optional[int] = None


class NutritionInfoCreate(NutritionInfoBase):
    pass


class NutritionInfo(NutritionInfoBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: Optional[str] = None
    video_url: str
    platform: str
    description: Optional[str] = None


class RecipeCreate(BaseModel):
    video_url: str
    model: Optional[str] = "gemini-3-flash-preview"  # Default to free tier model


class Recipe(RecipeBase):
    id: int
    thumbnail_path: Optional[str] = None
    video_path: Optional[str] = None
    created_at: datetime
    ingredients: List[Ingredient] = []
    steps: List[CookingStep] = []
    nutrition: Optional[NutritionInfo] = None

    class Config:
        from_attributes = True


class RecipeResponse(BaseModel):
    success: bool
    message: str
    recipe: Optional[Recipe] = None


class GroceryListItem(BaseModel):
    ingredient: str
    quantity: str
    stores: List[Dict[str, str]]


class GroceryList(BaseModel):
    recipe_id: int
    recipe_title: str
    items: List[GroceryListItem]
