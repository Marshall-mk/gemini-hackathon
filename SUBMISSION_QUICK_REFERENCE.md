# Recipe Extractor - Quick Submission Reference

## Elevator Pitch (50 characters max)

**Transform cooking videos into recipes in seconds**

## Elevator Pitch (Extended - 150 characters)

**Transform cooking videos into actionable recipes instantly. Paste a link, get ingredients, steps, nutrition info, and shopping links - no more pausing videos.**

---

## Built With (Tech Stack List)

### Core AI
- Google Gemini 3 Flash (free tier)
- Google Gemini 3 Pro (enhanced accuracy)
- High Thinking Mode (deep reasoning)
- High Media Resolution (visual analysis)

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- yt-dlp (TikTok videos)
- Instaloader (Instagram videos)
- OpenCV (video processing)
- ReportLab (PDF generation)

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Lucide React Icons
- Radix UI

### Database
- SQLite

---

## About The Project (Condensed - 200 words)

As a PhD student who recently started going to the gym, I needed to improve my cooking skills and track my nutrition - but I had no time to watch long cooking tutorials. I found myself constantly pausing Instagram and TikTok cooking videos to write down ingredients and steps. It was frustrating and inefficient.

That's when I built Recipe Extractor using Google Gemini 3.

The app takes a TikTok or Instagram cooking video URL and uses Gemini 3's multimodal capabilities to automatically extract everything: complete ingredient lists with quantities, step-by-step instructions, nutritional information (calories, protein, carbs, fats), and even shopping links to purchase ingredients.

I leveraged Gemini 3's **High Thinking Mode** for complex recipe reasoning and **High Media Resolution** for detailed visual ingredient identification. The result? What used to take me 20+ minutes of pausing, rewinding, and note-taking now takes 90 seconds.

The app has genuinely improved my life - I've extracted 50+ recipes, improved my cooking skills, and can now meal prep efficiently for my fitness goals. For any busy student, professional, or fitness enthusiast who wants to eat well without spending hours on meal prep research, this is a game changer.

---

## About The Project (Extended - 500 words)

### The Problem

As a PhD student, I'm constantly juggling research, classes, and personal health. Recently, I started taking fitness seriously and began going to the gym regularly. With this commitment came the need to improve my nutrition and learn to cook healthy meals.

I found myself scrolling through Instagram and TikTok, discovering amazing cooking videos with delicious, healthy recipes. But actually cooking from these videos was incredibly frustrating:

- Constantly pausing and rewinding to catch ingredients
- Frantically scribbling down measurements
- Losing track of cooking steps
- No nutritional information for macro tracking
- Having to search for ingredients separately

As someone trained to find efficient solutions, I thought: **"What if AI could watch these videos for me and extract everything I need?"**

### The Solution

Recipe Extractor leverages Google Gemini 3's advanced multimodal capabilities to automatically analyze cooking videos from Instagram and TikTok. In under 90 seconds, it:

1. **Extracts Complete Recipes**: Title, description, and every ingredient with precise quantities
2. **Generates Step-by-Step Instructions**: Clear, timed cooking steps in logical order
3. **Calculates Nutrition Information**: Calories, protein, carbs, fats, and fiber for meal planning
4. **Creates Shopping Lists**: Direct Amazon Fresh purchase links for each ingredient
5. **Saves Everything**: Beautiful PDF exports and a personal recipe collection

### Why Gemini 3?

I chose Gemini 3 Flash/Pro for several key reasons:

- **Native Video Understanding**: Analyzes videos directly without manual frame extraction
- **High Thinking Mode**: Deep reasoning for ingredient inference and understanding cooking techniques
- **High Media Resolution**: Reads text overlays and identifies ingredients visually
- **Long Context Window**: 1M tokens can handle long cooking videos
- **Cost-Effective**: Flash model offers 1,000 free requests per day

The **High Thinking Mode** was particularly valuable - it enables Gemini to infer ingredients shown but not mentioned, understand proper cooking sequencing, and estimate realistic nutritional values.

### Technical Implementation

The app uses a modern full-stack architecture:

**Backend**: FastAPI handles API requests, SQLAlchemy manages the recipe database, yt-dlp and Instaloader download videos from different platforms, OpenCV extracts thumbnails, and ReportLab generates PDF exports.

**Frontend**: React with TypeScript provides a type-safe, responsive UI built with Tailwind CSS and shadcn/ui components.

**AI Pipeline**: Videos are uploaded to Gemini 3 with high media resolution settings. The AI analyzes them using high thinking mode for deep reasoning. I use structured prompting to get JSON outputs with ingredients, steps, and nutrition information.

### Challenges Overcome

- **File Upload State Management**: Implemented async polling for Gemini's ACTIVE state
- **Structured Output**: Used regex and fallback parsing to extract JSON from AI responses
- **Path Normalization**: Solved Windows vs. web path inconsistencies (backslashes vs. forward slashes)
- **Nutritional Accuracy**: Increased thinking budget tokens to 10,000 for better estimates
- **Multi-Platform Support**: Unified TikTok and Instagram video downloading with different APIs

### Real Impact

Since building this, I've extracted 50+ recipes, significantly improved my cooking skills, started meal prepping efficiently, and tracked my macros accurately for gym progress. As a PhD student, every hour counts - Recipe Extractor has genuinely improved my quality of life.

For any busy student, professional, or fitness enthusiast who wants to eat well without spending hours on meal prep research, this is a game changer.

---

## Tags/Categories

- AI/ML
- Food & Cooking
- Health & Fitness
- Productivity
- Multimodal AI
- Video Analysis
- Recipe Management
- Nutrition Tracking
- Web Application
- Education

---

## Demo Video Script (2 minutes)

**[0:00 - 0:15] Hook**
"Ever see an amazing recipe video on Instagram or TikTok, but spending 20 minutes pausing and taking notes just to cook it? Let me show you a better way."

**[0:15 - 0:30] Problem**
"I'm a PhD student who recently started going to the gym. I need to eat healthy and track my nutrition, but I have zero time for lengthy cooking tutorials. Sound familiar?"

**[0:30 - 0:45] Solution Introduction**
"Meet Recipe Extractor - powered by Google Gemini 3. It watches cooking videos for you and extracts everything you need in 90 seconds."

**[0:45 - 1:00] Demo Start**
"Here's how it works. I found this delicious-looking recipe on Instagram. I just copy the URL..."

**[1:00 - 1:15] Demo - Paste & Extract**
"...paste it here, click Extract, and wait. Gemini 3 is now analyzing the video using high thinking mode and high media resolution."

**[1:15 - 1:30] Demo - Results**
"And done! Look at this - complete ingredient list with quantities, step-by-step instructions with timing, full nutritional breakdown, and shopping links for every ingredient."

**[1:30 - 1:45] Demo - Features**
"I can export this as a PDF, save it to my collection, or send the grocery list to my phone. All the recipes I've saved appear in this beautiful gallery."

**[1:45 - 2:00] Closing**
"Built with Google Gemini 3's multimodal AI, Recipe Extractor has saved me hours every week and helped me get fit while eating amazing food. Try it yourself - link in the description!"

---

## Screenshot Descriptions (for submission)

1. **Hero/Landing**: Clean UI with URL input box and "Extract Recipe" button
2. **Processing State**: Progress indicator showing Gemini 3 analyzing video
3. **Recipe Result**: Full recipe displayed with ingredients, steps, and nutrition
4. **Recipe Gallery**: Grid of recipe cards with thumbnails
5. **Recipe Detail**: Modal showing full recipe with shopping links
6. **PDF Export**: Generated PDF recipe card with beautiful formatting
7. **Settings Sidebar**: Dark mode toggle, API key input, model selection

---

## GitHub Repository Structure

```
recipe-extractor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # DB config
│   │   └── services/
│   │       ├── video_downloader.py
│   │       ├── gemini_service.py
│   │       ├── store_scraper.py
│   │       └── export_service.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── App.tsx
│   │   │   └── components/
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── SUBMISSION.md
├── README.md
└── LICENSE
```

---

## Installation Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

---

## API Key Instructions

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key
4. Add to `backend/.env`: `GEMINI_API_KEY=your_key_here`
5. Gemini 3 Flash: 1,000 free requests/day
6. Gemini 3 Pro: Paid tier, better accuracy

---

## Social Media Post Templates

### Twitter/X (280 chars)
Just built Recipe Extractor for the @GoogleDevs Gemini 3 Hackathon! 🍳🤖

Paste a cooking video URL → Get ingredients, steps, nutrition & shopping links in 90s.

Perfect for busy students & gym-goers who want to eat healthy without watching long tutorials.

#GeminiHackathon

### LinkedIn (longer)
Excited to share my Google Gemini 3 Hackathon project: Recipe Extractor! 🍳🤖

As a PhD student who recently started focusing on fitness, I struggled to find time for cooking tutorials. So I built an AI-powered app that transforms Instagram/TikTok cooking videos into actionable recipes in under 90 seconds.

Key features:
✅ Complete ingredient extraction with quantities
✅ Step-by-step instructions with timing
✅ Nutritional breakdown (calories, macros)
✅ Amazon Fresh shopping links for each ingredient
✅ PDF exports & recipe library

Built with Google Gemini 3's High Thinking Mode for deep recipe reasoning and High Media Resolution for visual ingredient identification.

This project has genuinely improved my meal prep efficiency and cooking skills. Check it out! [link]

#AI #Gemini #Hackathon #Cooking #HealthTech

---

## Frequently Asked Questions

**Q: Does it work with YouTube videos?**
A: Currently supports TikTok and Instagram. YouTube support is planned for future releases.

**Q: How accurate are the nutritional values?**
A: Using Gemini 3's High Thinking Mode, estimates are quite accurate for standard recipes. Always verify for strict dietary needs.

**Q: Can I use it without an API key?**
A: No, you need a Gemini API key. However, Gemini 3 Flash offers 1,000 free requests per day!

**Q: What about recipe copyright?**
A: The app extracts information for personal use, similar to taking notes while watching a video. Always credit original creators.

**Q: Does it handle multiple recipes in one video?**
A: Currently extracts the primary recipe. Multi-recipe support is planned.

**Q: Can I edit recipes after extraction?**
A: Not in the current version, but recipe editing is a planned feature.
