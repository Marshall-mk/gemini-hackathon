@echo off
echo ====================================
echo Recipe Extractor - Quick Deploy
echo ====================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing git repository...
    git init
    git branch -M main
    echo.
)

echo Adding all files to git...
git add .
echo.

echo Enter commit message (or press Enter for default):
set /p commit_msg="Commit message: "
if "%commit_msg%"=="" set commit_msg="Update Recipe Extractor"

git commit -m "%commit_msg%"
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo No remote found. Please enter your GitHub repository URL:
    echo Example: https://github.com/USERNAME/recipe-extractor.git
    set /p repo_url="Repository URL: "
    git remote add origin %repo_url%
)

echo Pushing to GitHub...
git push -u origin main
echo.

echo ====================================
echo Deployment Checklist:
echo ====================================
echo [ ] Code pushed to GitHub - DONE!
echo [ ] Deploy backend to Modal: cd backend ^&^& modal deploy modal_app.py
echo [ ] Deploy frontend to Vercel: vercel.com (import from GitHub)
echo [ ] Set VITE_API_BASE_URL in Vercel to your Modal URL
echo [ ] Test the live deployment
echo ====================================
echo.

pause
