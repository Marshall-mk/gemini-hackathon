# 🍳 Recipe Extractor - AI-Powered Cooking Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Extract cooking recipes from Instagram and TikTok videos using Google Gemini 3 AI! This application automatically analyzes cooking videos, extracts ingredients, cooking steps, nutritional information, and provides shopping links to purchase ingredients.

**🏆 Built for the Google Gemini 3 Hackathon**

## ✨ Features

- **🤖 AI-Powered Video Analysis**: Uses Google Gemini 3 Flash/Pro with advanced reasoning
- **📹 Multi-Platform Support**: Works with TikTok and Instagram videos
- **🥗 Complete Recipe Extraction**:
  - Recipe title and description
  - Complete ingredient list with quantities
  - Step-by-step cooking instructions with timing
  - Nutritional information (calories, protein, carbs, fats, fiber)
- **🛒 Smart Shopping**:
  - Generate grocery lists with store links
  - Direct shopping links to Instacart, Walmart, Amazon, Target
- **📦 Export Options**:
  - Beautiful PDF recipes with images
  - JSON export for data portability
- **🎥 Video Preview**: View original cooking video alongside recipe
- **🎨 Modern UI**: Beautiful, responsive interface with smooth animations
- **💾 Database**: Save and manage your recipe collection
- **🔄 Model Selection**: Choose between Gemini 3 Flash (free) or Pro (paid)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it free here](https://ai.google.dev/))
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/recipe-extractor.git
   cd recipe-extractor
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

   Simply open `frontend/index.html` in your browser

   OR use a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Then navigate to `http://localhost:3000`

### Windows Quick Start

Simply double-click `run.bat` in the project root to automatically:
- Create virtual environment
- Install dependencies
- Start the server

## 📖 Usage

1. **Get your Gemini API key**
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Create a new API key
   - Add it to `backend/.env`

2. **Select AI Model**
   - **Gemini 3 Flash** (Default): Free tier, 1,000 requests/day
   - **Gemini 3 Pro**: Paid tier, better accuracy

3. **Extract a Recipe**
   - Copy a TikTok or Instagram cooking video URL
   - Paste into the input field
   - Click "Extract Recipe"
   - Wait 30-90 seconds for AI analysis
   - View and save your recipe!

4. **Manage Recipes**
   - Browse your collection in the gallery
   - View video previews
   - Export to PDF or JSON
   - Generate grocery shopping lists
   - Delete unwanted recipes

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Google Gemini 3** - AI video analysis with deep reasoning
- **yt-dlp** - TikTok video downloading
- **Instaloader** - Instagram video downloading
- **ReportLab** - PDF generation
- **OpenCV** - Image/video processing

### Frontend
- **HTML5/CSS3/JavaScript** - Modern responsive design
- **Font Awesome** - Icons
- **Google Fonts** - Poppins typography

### AI Features
- **Gemini 3 Flash/Pro** - Video understanding
- **High Thinking Level** - Deep reasoning for complex recipes
- **High Media Resolution** - Detailed ingredient recognition
- **1M Token Context** - Process long cooking videos

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

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Video Download Issues
- Ensure video URLs are public
- Try different videos if one fails
- Check internet connection

### Gemini API Issues
- Verify API key in `.env`
- Check API quota at [Google AI Studio](https://ai.google.dev/)
- Gemini 3 Pro requires paid tier
- File processing takes 30-90 seconds

### Database Issues
- Delete `recipes.db` to reset
- Ensure write permissions in project directory

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini 3** - Advanced AI capabilities
- **FastAPI** - Excellent Python framework
- **yt-dlp & Instaloader** - Video downloading libraries
- **Gemini Hackathon** - Inspiration and motivation

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/recipe-extractor](https://github.com/yourusername/recipe-extractor)

## 🔮 Future Enhancements

- [ ] Voice commands for hands-free extraction
- [ ] Meal planning from saved recipes
- [ ] Recipe variations (vegan, gluten-free)
- [ ] Cost estimation for ingredients
- [ ] Cooking timers integration
- [ ] Mobile app (iOS/Android)
- [ ] Social sharing features
- [ ] Recipe ratings and reviews
- [ ] Multi-language support
- [ ] Ingredient substitution suggestions

---

**Built with ❤️ using Google Gemini 3**

⭐ Star this repo if you find it helpful!
