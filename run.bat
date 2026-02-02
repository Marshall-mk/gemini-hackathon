@echo off
echo ===================================
echo Recipe Extractor - Starting Server
echo ===================================
echo.

cd backend

echo Checking if virtual environment exists...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo Open frontend/index.html in your browser to use the app
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
