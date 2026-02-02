# 🚀 Quick Deployment Guide - Recipe Extractor

## Overview

This guide will help you deploy Recipe Extractor online in ~30 minutes:
- **Backend**: Modal (Python serverless platform)
- **Frontend**: Vercel (React hosting)
- **Code**: GitHub

---

## Part 1: Push to GitHub (5 minutes)

### Step 1: Initialize Git Repository

```bash
cd C:\Users\User\Desktop\.dev\hackathon

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Recipe Extractor for Gemini 3 Hackathon"
```

### Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `recipe-extractor` (or `gemini-hackathon`)
3. Description: "AI-powered recipe extractor using Google Gemini 3"
4. Keep it **Public** (required for free Vercel deployment)
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/recipe-extractor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Your code is now on GitHub!**

---

## Part 2: Deploy Backend to Modal (10 minutes)

Modal is perfect for temporary Python deployments - serverless, fast, and free tier available.

### Step 1: Install Modal CLI

```bash
pip install modal
```

### Step 2: Create Modal Account & Login

```bash
# This will open a browser for authentication
modal setup
```

Sign up at modal.com if you don't have an account (free tier is generous).

### Step 3: Create Modal Deployment File

I'll create this file for you - it will set up your FastAPI app on Modal.

### Step 4: Set Modal Secrets

```bash
# Add your Gemini API key as a Modal secret
modal secret create gemini-api-key GEMINI_API_KEY=your_actual_gemini_key_here
```

### Step 5: Deploy to Modal

```bash
cd backend
modal deploy modal_app.py
```

Modal will give you a public URL like: `https://your-username--recipe-extractor-fastapi-app.modal.run`

**✅ Your backend is now live!**

---

## Part 3: Deploy Frontend to Vercel (10 minutes)

### Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub (easiest option)
3. Authorize Vercel to access your repositories

### Step 2: Import Project

1. Click "Add New Project"
2. Select your `recipe-extractor` repository
3. Vercel will auto-detect it's a Vite project

### Step 3: Configure Build Settings

**Framework Preset**: Vite

**Root Directory**: `frontend`

**Build Command**: `npm run build`

**Output Directory**: `dist`

**Install Command**: `npm install`

### Step 4: Add Environment Variable

In Vercel dashboard, add environment variable:

**Key**: `VITE_API_BASE_URL`

**Value**: Your Modal backend URL (e.g., `https://your-username--recipe-extractor-fastapi-app.modal.run`)

### Step 5: Deploy

Click "Deploy" - Vercel will build and deploy automatically (~2 minutes)

You'll get a URL like: `https://recipe-extractor-xyz.vercel.app`

**✅ Your frontend is now live!**

---

## Part 4: Test Your Deployment (5 minutes)

1. Visit your Vercel URL
2. Open browser console (F12) to check for errors
3. Paste a TikTok or Instagram cooking video URL
4. Click "Extract Recipe"
5. Verify it works!

### Common Issues

**CORS Errors**: Modal automatically handles CORS, but if you see issues:
- Check that your backend URL in Vercel env vars is correct
- Ensure no trailing slash in the URL

**API Key Issues**:
- Verify your Modal secret is set correctly
- Check Modal logs: `modal app logs`

**File Upload Issues**:
- Modal has ephemeral storage - files are temporary (perfect for your use case)
- Videos/images will be processed but not permanently stored

---

## Part 5: Update README with Live Links (2 minutes)

Add this to your README.md:

```markdown
## 🌐 Live Demo

**Frontend**: https://your-app.vercel.app
**Backend API**: https://your-backend.modal.run
**GitHub**: https://github.com/YOUR_USERNAME/recipe-extractor

Try it now! Just paste a cooking video URL and watch the magic happen.
```

---

## Alternative: Railway (Backend Alternative to Modal)

If Modal doesn't work for you, Railway is another quick option:

### Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Choose the `backend` directory
6. Add environment variables:
   - `GEMINI_API_KEY`: your key
   - `PORT`: 8000
7. Railway will auto-detect FastAPI and deploy

Railway gives you a URL like: `https://recipe-extractor.railway.app`

---

## Costs & Limits (Free Tier)

### Modal (Recommended)
- **Free Tier**: $30/month credits
- Serverless billing: pay only when API is called
- Perfect for hackathon demos
- **Estimated cost**: $0-5 for hackathon period

### Vercel
- **Free Tier**: Unlimited for personal projects
- 100 GB bandwidth/month
- Perfect for frontend hosting
- **Cost**: $0

### Railway (Alternative)
- **Free Tier**: $5 credit/month
- Can run continuously
- **Estimated cost**: $0-5 for hackathon period

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Modal account created and CLI setup
- [ ] Gemini API key added to Modal secrets
- [ ] Backend deployed to Modal
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Environment variable set in Vercel
- [ ] Tested live deployment
- [ ] README updated with live links
- [ ] Submission includes live demo URL

---

## Important Notes for Submission

1. **Persistence**: Modal uses ephemeral storage, so:
   - Recipes are stored in SQLite in memory
   - Videos/images are temporary
   - Perfect for demo, but database resets on cold starts

2. **Cold Starts**: Modal may have 2-5 second cold starts if idle
   - First request after idle might be slow
   - Subsequent requests are fast

3. **For Permanent Hosting** (after hackathon):
   - Use Railway or Render for backend
   - Add PostgreSQL database
   - Use AWS S3 or Cloudinary for file storage

---

## Support

If you encounter issues:

**Modal Docs**: https://modal.com/docs
**Vercel Docs**: https://vercel.com/docs
**Railway Docs**: https://docs.railway.app

**Common Commands**:
```bash
# Check Modal logs
modal app logs

# Redeploy Modal
modal deploy modal_app.py

# Redeploy Vercel (push to GitHub)
git add .
git commit -m "Update"
git push
```

---

Good luck with your submission! 🚀
