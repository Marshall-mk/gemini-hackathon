# Quick Start Guide

Get your Recipe Extractor running in 5 minutes!

## Step 1: Verify Your API Key

Your Gemini API key is already configured in `backend/.env.example`:
```
GEMINI_API_KEY=......
```

Copy this file to `.env`:
```bash
cd backend
cp .env.example .env
```

## Step 2: Run the Application

### Option A: Using the Run Script (Windows)

Simply double-click `run.bat` in the project root, or run:
```bash
run.bat
```

This will automatically:
- Create a virtual environment
- Install all dependencies
- Start the FastAPI server

### Option B: Manual Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload
```

## Step 3: Open the Frontend

1. Navigate to the `frontend` folder
2. Open `index.html` in your web browser

OR use a simple HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Then open: `http://localhost:3000`

## Step 4: Extract Your First Recipe!

1. Find a cooking video on TikTok or Instagram
2. Copy the URL
3. Paste it into the Recipe Extractor
4. Click "Extract Recipe"
5. Wait 30-60 seconds for AI magic!

## Test URLs

Try these platforms:
- **TikTok**: Search for `@cookingvideos` or any cooking content creator
- **Instagram**: Look for reels with `#cooking` or `#recipe`

## Common Issues

### "Module not found" error
```bash
# Make sure you're in the virtual environment
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### "Database error"
The database is created automatically. If issues persist:
```bash
# Delete the database and restart
rm recipes.db
python -m uvicorn app.main:app --reload
```

### "Cannot download video"
- Ensure the video is public
- Try a different video URL
- Check your internet connection

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## What to Show in Your Demo

1. **Paste a video URL** - Show the simple interface
2. **Watch the extraction** - Highlight the AI processing
3. **View the recipe** - Show ingredients, steps, nutrition
4. **Grocery list** - Demonstrate shopping links
5. **Export PDF** - Show the beautiful PDF output

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at `/docs`
- Customize the frontend styling
- Add more features!

---

**Ready to wow the judges? Let's go!** 🚀
