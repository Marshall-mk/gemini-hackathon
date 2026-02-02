# Recipe Extractor - AI-Powered Cooking Assistant

## 🎯 Elevator Pitch

**Transform cooking videos into actionable recipes in seconds. Just paste a link, get ingredients, steps, nutrition info, and instant shopping links - no more pausing and rewinding videos.**

---

## 📖 About The Project

### The Inspiration

As a PhD student, my life is a constant juggling act between research, classes, and trying to maintain a healthy lifestyle. Recently, I started taking my fitness seriously and began going to the gym regularly. With this new commitment came a crucial realization: I needed to take control of my nutrition and improve my cooking skills.

The problem? Time - or the lack of it.

I found myself scrolling through Instagram and TikTok, discovering amazing cooking videos with healthy, delicious recipes. But the process of actually cooking from these videos was frustrating:

- Constantly pausing and rewinding to catch ingredients
- Frantically scribbling down measurements while the video played
- Losing track of cooking steps
- No idea about nutritional content
- Having to search for ingredients online separately

As someone in academia, I'm trained to find efficient solutions to problems. I thought: **"What if AI could watch these videos for me and extract everything I need?"**

That's when I discovered Google Gemini 3's multimodal capabilities, and Recipe Extractor was born.

### What It Does

Recipe Extractor leverages Google Gemini 3's advanced video understanding capabilities to automatically analyze cooking videos from Instagram and TikTok. In under 90 seconds, it:

1. **Extracts Complete Recipes**: Title, description, and every ingredient with precise quantities
2. **Generates Step-by-Step Instructions**: Clear, timed cooking steps in logical order
3. **Calculates Nutrition Information**: Calories, protein, carbs, fats, and fiber for meal planning
4. **Creates Shopping Lists**: Direct Amazon Fresh purchase links for each ingredient
5. **Saves Everything**: Beautiful PDF exports and a personal recipe collection

For a busy PhD student who needs to meal prep efficiently, track macros for fitness goals, and actually learn to cook properly - this is a game changer.

### How I Built It

#### Architecture Overview

The project uses a modern full-stack architecture:

**Backend (Python)**
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM for recipe database management
- **Google Gemini 3 Flash/Pro**: Core AI engine for video analysis
- **yt-dlp & Instaloader**: Video downloading from TikTok and Instagram
- **OpenCV**: Video frame extraction and thumbnail generation
- **ReportLab**: PDF recipe generation

**Frontend (React + TypeScript)**
- **React 18**: Modern component-based UI
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Responsive, beautiful styling
- **shadcn/ui**: High-quality component library
- **Vite**: Lightning-fast build tool

#### The Gemini 3 Integration

The heart of the application is the Gemini 3 integration, which I carefully optimized:

```python
# High Thinking Level for complex recipe reasoning
generation_config = {
    "thinking": {
        "mode": "HIGH",
        "type": "THINKING"
    },
    "response_modalities": ["TEXT"]
}

# High media resolution for detailed ingredient identification
file = genai.upload_file(
    video_path,
    config={
        "media_resolution": "HIGH",
        "thinking_config": {
            "thinking_budget_tokens": 10000
        }
    }
)
```

I use Gemini 3's **high thinking mode** to enable deep reasoning about:
- Ingredient inference from visual cues (e.g., "a pinch of salt" when shown but not mentioned)
- Multi-step cooking process understanding
- Nutritional estimation based on visible portions

The **high media resolution** setting allows Gemini to:
- Read text overlays in videos (many creators show measurements as text)
- Identify ingredients from visual appearance
- Estimate quantities from visual context

#### Video Processing Pipeline

1. **URL Detection**: Parse TikTok/Instagram URLs
2. **Video Download**: Platform-specific downloaders (yt-dlp for TikTok, Instaloader for Instagram)
3. **Thumbnail Extraction**: OpenCV captures first frame for gallery preview
4. **File Upload to Gemini**: Upload video with ACTIVE state polling
5. **AI Analysis**: Gemini 3 analyzes with structured JSON prompting
6. **Data Parsing**: Extract and validate recipe data
7. **Store Enrichment**: Generate shopping links for each ingredient
8. **Database Storage**: Save with SQLite for persistence
9. **PDF Generation**: Create printable recipe cards with ReportLab

#### The Challenges I Faced

**1. File Upload State Management**

Gemini's file upload API requires polling for ACTIVE state before use:

```python
while file.state.name == "PROCESSING":
    await asyncio.sleep(2)
    file = genai.get_file(file.name)

if file.state.name != "ACTIVE":
    raise Exception("File processing failed")
```

I had to implement proper async/await patterns to avoid blocking the API.

**2. Structured Output Parsing**

Getting consistent JSON output from AI is notoriously difficult. I solved this by:
- Explicitly requesting JSON in the prompt
- Using regex to extract JSON from markdown code blocks
- Implementing fallback parsing with `json.loads()`
- Validating all fields with Pydantic schemas

**3. Video Download Platform Differences**

TikTok and Instagram have completely different APIs:
- TikTok uses yt-dlp with simple video IDs
- Instagram requires shortcode extraction and returns timestamp-based filenames
- Had to normalize file paths across platforms for consistent storage

**4. Path Normalization (Windows vs Web)**

Windows uses backslashes (`\`) while web URLs use forward slashes (`/`). This caused thumbnail display issues:

```python
# Solution: Convert all paths to web-safe format
def _to_public_path(self, file_path: Path) -> str:
    relative = file_path.relative_to(self.data_dir)
    # Always use forward slashes for web
    return f"{relative.parts[0]}/" + "/".join(relative.parts[1:])
```

**5. Nutritional Information Accuracy**

Gemini 3's high thinking mode was crucial here. Initial attempts gave wildly inaccurate calorie counts. By:
- Increasing thinking budget tokens to 10,000
- Explicitly asking for reasoning about portion sizes
- Requesting per-serving calculations

I achieved much more realistic nutritional estimates.

**6. Shopping Link Generation**

Amazon Fresh search URL integration required:
- URL-encoding ingredient names properly for special characters
- Cleaning ingredient names (removing "fresh", "dried", etc.) for better search results
- Simplifying to a single store to avoid UI clutter

```python
encoded_ingredient = urllib.parse.quote(ingredient_name)
amazon_url = f"https://www.amazon.com/s?k={encoded_ingredient}"
```

**7. Storage Optimization**

Video files are large (10-100 MB each). I implemented automatic cleanup:
- Videos are deleted immediately after processing
- Only thumbnails are retained (200-500 KB each)
- Saves 95%+ storage space
- Critical for serverless deployments (Modal/Railway have limited storage)

```python
# Cleanup after successful extraction
video_downloader.cleanup_video(video_path)
```

This reduces hosting costs and makes the app practical for long-term use.

**8. React State Management**

Managing the complex state of:
- Recipe extraction progress
- Gallery updates
- Dialog navigation
- Error handling

I used React hooks effectively with `useState` for local state and careful prop drilling for the recipe detail dialog.

### What I Learned

**Technical Skills**
- Deep understanding of **Google Gemini 3 API** and multimodal AI
- Async programming in Python with `asyncio`
- React + TypeScript for production-grade frontends
- Video processing with OpenCV
- Web scraping and API reverse engineering

**AI Engineering**
- Prompt engineering for structured outputs
- The importance of **thinking modes** for complex reasoning tasks
- Media resolution settings impact on AI accuracy
- Token budget optimization for cost-effective API usage

**Product Development**
- The power of solving your own problems (dogfooding)
- User experience matters - even for personal projects
- Importance of error handling and graceful degradation
- Making AI features feel fast and responsive

### Why Gemini 3?

I evaluated several AI models for this project:

- **OpenAI GPT-4 Vision**: Expensive, limited video support
- **Claude 3.5 Sonnet**: Excellent for text, but no native video analysis
- **Gemini 3 Flash/Pro**: Perfect for this use case

Gemini 3 won because:

1. **Native Video Understanding**: No need to extract frames manually
2. **Long Context Window**: 1M tokens - can handle long cooking videos
3. **High Thinking Mode**: Deep reasoning for ingredient inference
4. **Cost-Effective**: Flash model is free tier with 1,000 requests/day
5. **High Media Resolution**: Detailed visual analysis for ingredients
6. **Multimodal Output**: Text extraction from video overlays

The **high thinking mode** was particularly valuable - it enabled Gemini to:
- Infer ingredients shown but not mentioned verbally
- Understand cooking techniques and proper sequencing
- Estimate realistic nutritional values
- Handle ambiguous quantities ("a handful", "to taste")

### Real-World Impact

Since building this, I've:
- Extracted 50+ recipes from my saved Instagram videos
- Improved my cooking skills significantly
- Started meal prepping efficiently for the gym
- Tracked my macros more accurately
- Saved hours of time each week

As a PhD student, every hour counts. Recipe Extractor has genuinely improved my quality of life.

### Future Enhancements

- **Meal Planning**: Generate weekly meal plans based on saved recipes
- **Voice Commands**: Hands-free extraction while cooking
- **Recipe Variations**: Generate vegan, gluten-free, or low-carb alternatives
- **Cost Estimation**: Calculate total grocery cost before shopping
- **Mobile App**: iOS/Android for on-the-go recipe saving
- **Social Features**: Share recipes with friends and family
- **Cooking Timers**: Integrated timers synced with recipe steps
- **Ingredient Substitutions**: AI-powered alternatives for missing ingredients

---

## 🛠️ Built With

### AI & Machine Learning
- **Google Gemini 3 Flash** - Primary AI model (free tier)
- **Google Gemini 3 Pro** - Enhanced accuracy (paid tier)
- **High Thinking Mode** - Deep reasoning for complex recipes
- **High Media Resolution** - Detailed visual analysis

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation and schemas
- **yt-dlp** - TikTok video downloading
- **Instaloader** - Instagram video downloading
- **OpenCV (cv2)** - Video processing and thumbnail extraction
- **ReportLab** - PDF generation
- **python-dotenv** - Environment configuration

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Component library
- **Lucide React** - Icon library
- **Radix UI** - Accessible component primitives

### Database & Storage
- **SQLite** - Lightweight database
- **File System** - Video and image storage

### Development Tools
- **Git** - Version control
- **VS Code** - Code editor
- **Python Virtual Environment** - Dependency isolation
- **ESLint & Prettier** - Code quality and formatting

---

## 🏆 Hackathon Highlights

### Gemini 3 Features Showcased

1. **Multimodal Video Understanding**: Full video analysis without frame extraction
2. **High Thinking Mode**: Complex reasoning for ingredient inference and nutrition
3. **High Media Resolution**: Detailed visual ingredient identification
4. **Long Context**: 1M tokens for processing lengthy cooking videos
5. **Structured Output**: JSON generation for programmatic recipe extraction
6. **Text Recognition**: Reading overlay text in videos

### Innovation

- **End-to-End Solution**: From video URL to printable recipe in under 90 seconds
- **Multi-Platform Support**: Works with both TikTok and Instagram
- **Smart Shopping Integration**: Direct purchase links for every ingredient
- **Production-Ready UI**: Beautiful, responsive React interface
- **Comprehensive Nutrition**: Full macro tracking for fitness enthusiasts
- **Persistent Storage**: Build a personal recipe library over time

---

## 🚀 Try It Yourself

```bash
# Clone the repository
git clone https://github.com/yourusername/recipe-extractor.git
cd recipe-extractor

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Add your Gemini API key to .env
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the server
python -m uvicorn app.main:app --reload

# In another terminal, run the frontend
cd ../frontend
npm install
npm run dev
```

Visit `http://localhost:5173` and start extracting recipes!

---

## 📝 License

MIT License - feel free to use this for your own cooking adventures!

---

**Built with ❤️ and Google Gemini 3 for the Google Gemini 3 Hackathon**

*Making healthy cooking accessible, one video at a time.*
