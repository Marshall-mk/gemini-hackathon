from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=True)
    video_url = Column(String(1000), nullable=False, unique=True)
    platform = Column(String(50), nullable=False)  # 'instagram' or 'tiktok'
    thumbnail_path = Column(String(500), nullable=True)
    video_path = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    steps = relationship("CookingStep", back_populates="recipe", cascade="all, delete-orphan")
    nutrition = relationship("NutritionInfo", back_populates="recipe", uselist=False, cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String(200), nullable=False)
    quantity = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=True)
    store_links = Column(JSON, nullable=True)  # Store as JSON array

    recipe = relationship("Recipe", back_populates="ingredients")


class CookingStep(Base):
    __tablename__ = "cooking_steps"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=False)
    duration = Column(String(50), nullable=True)  # e.g., "5 minutes"

    recipe = relationship("Recipe", back_populates="steps")


class NutritionInfo(Base):
    __tablename__ = "nutrition_info"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False, unique=True)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fats = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    servings = Column(Integer, nullable=True)

    recipe = relationship("Recipe", back_populates="nutrition")
