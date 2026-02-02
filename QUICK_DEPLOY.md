# ⚡ Quick Deploy Reference Card

## 🎯 Goal: Get Your App Online in 30 Minutes

---

## Step 1: Push to GitHub (5 min)

```bash
# Option 1: Use the deploy script
deploy.bat

# Option 2: Manual
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/recipe-extractor.git
git push -u origin main
```

**GitHub Repo**: https://github.com/YOUR_USERNAME/recipe-extractor

---

## Step 2: Deploy Backend (10 min)

### Option A: Modal (Recommended - Serverless)

```bash
# Install Modal
pip install modal

# Login to Modal
modal setup

# Add your Gemini API key
modal secret create gemini-api-key GEMINI_API_KEY=your_key_here

# Deploy
cd backend
modal deploy modal_app.py
```

**Your Backend URL**: `https://YOUR_USERNAME--recipe-extractor-fastapi-app.modal.run`

### Option B: Railway (Alternative - Always On)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `recipe-extractor` repo
4. Set root directory to `backend`
5. Add environment variable: `GEMINI_API_KEY=your_key_here`
6. Click Deploy

**Your Backend URL**: `https://recipe-extractor-production.up.railway.app`

---

## Step 3: Deploy Frontend (10 min)

### Vercel (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "Add New Project"
4. Select `recipe-extractor` repo
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add Environment Variable:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `your_modal_or_railway_backend_url` (from Step 2)
7. Click "Deploy"

**Your Frontend URL**: `https://recipe-extractor.vercel.app`

---

## Step 4: Test (5 min)

1. Visit your Vercel URL
2. Paste a cooking video URL (TikTok or Instagram)
3. Click "Extract Recipe"
4. Verify it works!

---

## 📋 Deployment Checklist

- [ ] GitHub repo created and code pushed
- [ ] Backend deployed (Modal or Railway)
- [ ] Backend URL copied
- [ ] Frontend deployed to Vercel
- [ ] `VITE_API_BASE_URL` set in Vercel
- [ ] Live site tested and working
- [ ] README updated with live demo link

---

## 🔑 Important URLs

| Service | Purpose | URL |
|---------|---------|-----|
| GitHub | Code hosting | https://github.com/YOUR_USERNAME/recipe-extractor |
| Modal | Backend hosting | https://modal.com/dashboard |
| Railway | Alt backend | https://railway.app/dashboard |
| Vercel | Frontend hosting | https://vercel.com/dashboard |
| Google AI Studio | Gemini API key | https://ai.google.dev/ |

---

## 🐛 Troubleshooting

### Backend not responding
```bash
# Check Modal logs
modal app logs

# Redeploy Modal
modal deploy modal_app.py

# Check Railway logs
# Go to Railway dashboard → View Logs
```

### Frontend can't connect to backend
1. Check `VITE_API_BASE_URL` in Vercel environment variables
2. Make sure no trailing slash in URL
3. Verify backend is running (visit `backend-url/docs`)

### CORS errors
- Modal handles CORS automatically
- For Railway, CORS is configured in `main.py`

### API key issues
```bash
# Re-add Modal secret
modal secret create gemini-api-key GEMINI_API_KEY=your_key_here

# For Railway, update environment variable in dashboard
```

---

## 💰 Cost Estimate (Free Tier)

| Service | Free Tier | Estimated Cost |
|---------|-----------|----------------|
| GitHub | Unlimited public repos | $0 |
| Modal | $30/month credits | $0-5 |
| Railway | $5/month credits | $0-5 |
| Vercel | Unlimited for hobby | $0 |
| **Total** | | **$0-5** |

---

## 🎓 For Hackathon Submission

### Add to README.md:

```markdown
## 🌐 Live Demo

**🚀 Try it now**: [https://recipe-extractor.vercel.app](https://your-actual-url.vercel.app)

**Backend API**: [https://your-backend.modal.run/docs](https://your-actual-backend.modal.run/docs)

**GitHub**: [https://github.com/YOUR_USERNAME/recipe-extractor](https://your-actual-repo)
```

### For Submission Form:

**Demo URL**: `https://recipe-extractor.vercel.app`

**GitHub Repo**: `https://github.com/YOUR_USERNAME/recipe-extractor`

**Video Demo**: (Record a 2-minute walkthrough showing the app in action)

---

## 📺 Quick Demo Recording Tips

1. **Open your live site**: Show the URL in browser
2. **Paste a cooking video**: Use a popular TikTok/Instagram recipe
3. **Show the extraction**: Let it process (speeds up video if needed)
4. **Highlight features**: Ingredients, steps, nutrition, shopping links
5. **Show PDF export**: Download and show the PDF
6. **Show recipe gallery**: Browse saved recipes

**Tools**:
- OBS Studio (free) - https://obsproject.com/
- Loom (easy) - https://loom.com/
- Screen recording built into Windows (Win + G)

---

## 🚀 Commands Summary

```bash
# Deploy to GitHub
git add . && git commit -m "Update" && git push

# Deploy to Modal
cd backend && modal deploy modal_app.py

# Check Modal logs
modal app logs

# Redeploy Vercel (just push to GitHub)
git push
```

---

**Good luck with your submission!** 🎉

If you get stuck, check the full `DEPLOYMENT_GUIDE.md` for detailed instructions.
