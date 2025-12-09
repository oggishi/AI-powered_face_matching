@echo off
echo ========================================
echo  Quick Start - AI Face Matching
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "face_env\" (
    echo Creating virtual environment...
    python -m venv face_env
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call face_env\Scripts\activate.bat
echo.

REM Install packages
echo Installing packages...
call install_windows.bat
if %errorlevel% neq 0 (
    echo.
    echo Installation failed. Please check the error above.
    pause
    exit /b 1
)

REM Run the application
echo.
echo ========================================
echo  Starting application...
echo ========================================
echo.
python main.py

pause
