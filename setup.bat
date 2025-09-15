@echo off
echo Installing Araiza Inc Website Dependencies...
echo.

echo Step 1: Installing Python packages...
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 python-dotenv==1.0.0 requests==2.31.0

if %errorlevel% neq 0 (
    echo Error installing packages. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo Step 2: Dependencies installed successfully!
echo.
echo Step 3: Starting the application...
python app.py

pause