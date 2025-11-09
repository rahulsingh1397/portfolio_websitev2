@echo off
echo ========================================
echo Testing Blog Automation Locally
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo IMPORTANT: Set your API keys
echo ========================================
echo.
set /p DEEPSEEK_KEY="Enter your DeepSeek API key: "
set /p NEWS_KEY="Enter your NewsAPI key (or press Enter to skip): "

set DEEPSEEK_API_KEY=%DEEPSEEK_KEY%
if not "%NEWS_KEY%"=="" set NEWSAPI_KEY=%NEWS_KEY%

echo.
echo ========================================
echo Running blog generator...
echo ========================================
echo.

python generate_blog.py

echo.
echo ========================================
echo Done! Check the blog/ folder for output
echo ========================================
pause
