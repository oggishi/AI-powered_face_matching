@echo off
REM 🐳 Quick Docker Launcher for Windows

echo ================================================
echo  AI-Powered Face Matching - Docker Launcher
echo ================================================
echo.

echo [1] Production Mode (Optimized)
echo [2] Development Mode (Hot-Reload)
echo [3] Stop All Containers
echo [4] View Logs
echo [5] Clean Everything
echo.

set /p choice="Select option (1-5): "

if "%choice%"=="1" goto production
if "%choice%"=="2" goto development
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto clean

echo Invalid option!
pause
exit /b

:production
echo.
echo Starting in PRODUCTION mode...
docker-compose up -d --build
echo.
echo ✅ Server running at http://localhost:8000
echo.
echo View logs: docker-compose logs -f
pause
exit /b

:development
echo.
echo Starting in DEVELOPMENT mode (hot-reload)...
docker-compose -f docker-compose.dev.yml up --build
pause
exit /b

:stop
echo.
echo Stopping all containers...
docker-compose down
docker-compose -f docker-compose.dev.yml down
echo ✅ All containers stopped
pause
exit /b

:logs
echo.
echo Showing logs (Ctrl+C to exit)...
docker-compose logs -f
pause
exit /b

:clean
echo.
echo ⚠️  WARNING: This will remove all containers, volumes, and cached data!
set /p confirm="Are you sure? (yes/no): "
if not "%confirm%"=="yes" exit /b

echo.
echo Cleaning everything...
docker-compose down -v
docker-compose -f docker-compose.dev.yml down -v
docker system prune -af --volumes
echo ✅ Cleanup complete
pause
exit /b
