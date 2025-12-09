@echo off
echo ========================================
echo  AI Face Matching - Windows Installer
echo ========================================
echo.

REM Upgrade pip first
echo [1/3] Upgrading pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
echo.

REM Install core packages first
echo [2/3] Installing core packages...
pip install numpy
pip install Pillow
pip install opencv-python
if %errorlevel% neq 0 (
    echo ERROR: Failed to install core packages
    pause
    exit /b 1
)
echo.

REM Install remaining packages
echo [3/3] Installing remaining packages...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install scikit-learn==1.3.2
pip install mediapipe==0.10.8
pip install "sqlalchemy>=2.0.35"
pip install python-dotenv==1.0.0
pip install aiofiles==23.2.1
pip install jinja2==3.1.2
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installation completed successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Run: python main.py
echo   2. Open: http://localhost:8000
echo.
pause
