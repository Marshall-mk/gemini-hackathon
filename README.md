# 🍳 Recipe Extractor - AI-Powered Cooking Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![React](https://img.shields.io/badge/React-18-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg)
![Gemini](https://img.shields.io/badge/Gemini-3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Transform cooking videos into actionable recipes in seconds. Just paste a link, get ingredients, steps, nutrition, and shopping links—no more pausing and rewinding.**

**🏆 Built for the Google Gemini 3 Hackathon**

Stop spending 20+ minutes pausing cooking videos to copy down ingredients! Recipe Extractor uses Google Gemini 3's multimodal AI to automatically analyze cooking videos from Instagram and TikTok, extracting everything you need to cook delicious meals—in under 90 seconds.

## ✨ Features

### 🤖 AI-Powered Video Analysis
- **Google Gemini 3 Flash/Pro** with High Thinking Mode for deep recipe reasoning
- **High Media Resolution** for detailed ingredient identification from visual cues
- **1M Token Context** to process long cooking videos without truncation
- Reads text overlays in videos automatically

### 📹 Multi-Platform Support
- **TikTok** videos via URL
- **Instagram** Reels and posts via URL
- Automatic platform detection

### 🥗 Complete Recipe Extraction
- ✅ Recipe title and description
- ✅ Complete ingredient list with precise quantities and units
- ✅ Step-by-step cooking instructions with timing estimates
- ✅ Full nutritional breakdown (calories, protein, carbs, fats, fiber, servings)
- ✅ Ingredient inference from visual context (even if not mentioned verbally)

### 🛒 Smart Shopping
- **Amazon Fresh** integration with direct purchase links for each ingredient
- One-click access to buy any ingredient
- Ingredient name cleaning for optimal search results
- Bulk shopping list generation

### 📦 Export & Save
- 📄 Beautiful PDF recipes with images and formatting
- 💾 JSON export for data portability
- 🗂️ Personal recipe library with thumbnails
- 🔍 Recipe gallery with search and filtering
- 💿 **Smart Storage**: Automatically deletes videos after processing (keeps only thumbnails to save space)

### 🎨 Modern User Experience
- Beautiful, responsive React + TypeScript frontend
- Dark/Light mode support
- Real-time processing progress
- Smooth animations and transitions
- Mobile-friendly design

### ⚙️ Flexible Configuration
- Choose between Gemini 3 Flash (free, 1,000 requests/day) or Pro (paid, enhanced accuracy)
- Custom API key support
- Configurable model selection

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it free here](https://ai.google.dev/))
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/marshall-mk/gemini-hackathon.git
   cd gemini-hackathon
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the backend**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   Backend will be available at: `http://localhost:8000`

   API docs: `http://localhost:8000/docs`

5. **Open the frontend**
   ```bash
   cd frontend
   npm install && npm run dev
   ```
   Then navigate to `http://localhost:5175`

### Windows Quick Start

Simply double-click `run.bat` in the project root to automatically:
- Create virtual environment
- Install dependencies
- Start the server


## 📁 Project Structure

```
recipe-extractor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # DB configuration
│   │   └── services/
│   │       ├── video_downloader.py
│   │       ├── gemini_service.py
│   │       ├── store_scraper.py
│   │       └── export_service.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── data/
│   ├── videos/
│   ├── images/
│   └── exports/
├── .gitignore
├── README.md
├── LICENSE
└── run.bat (Windows quick start)
```

## 🔌 API Endpoints

### Recipes
- `POST /api/recipes/extract` - Extract recipe from video URL
- `GET /api/recipes` - Get all recipes
- `GET /api/recipes/{id}` - Get specific recipe
- `DELETE /api/recipes/{id}` - Delete recipe

### Export
- `GET /api/recipes/{id}/export/json` - Export as JSON
- `GET /api/recipes/{id}/export/pdf` - Export as PDF

### Grocery
- `GET /api/recipes/{id}/grocery-list` - Get shopping list with store links

### Health
- `GET /api/health` - Health check
- `GET /` - API info

Full API documentation available at `/docs` when server is running.

## 🎯 Gemini 3 Features

This project leverages the latest Gemini 3 capabilities:

### High Thinking Level
- Deep reasoning for complex recipe extraction
- Multi-step cooking process understanding
- Ingredient inference from context

### High Media Resolution
- Detailed visual ingredient identification
- Text overlay reading from videos
- Quantity estimation from visual cues

### Advanced Configuration
- Adaptive temperature for different tasks
- Task-specific optimization
- File upload with ACTIVE state polling

## 🌟 Screenshots

[Add your screenshots here]


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini 3** - Advanced AI capabilities
- **FastAPI** - Excellent Python framework
- **yt-dlp & Instaloader** - Video downloading libraries
- **Gemini Hackathon** - Inspiration and motivation

---

**Built with ❤️ using Google Gemini 3**

⭐ Star this repo if you find it helpful!
