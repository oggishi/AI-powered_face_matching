#!/bin/bash
# 🐳 Quick Docker Launcher for Linux/Mac

echo "================================================"
echo "  AI-Powered Face Matching - Docker Launcher"
echo "================================================"
echo ""

echo "[1] Production Mode (Optimized)"
echo "[2] Development Mode (Hot-Reload)"
echo "[3] Stop All Containers"
echo "[4] View Logs"
echo "[5] Clean Everything"
echo ""

read -p "Select option (1-5): " choice

case $choice in
  1)
    echo ""
    echo "Starting in PRODUCTION mode..."
    docker-compose up -d --build
    echo ""
    echo "✅ Server running at http://localhost:8000"
    echo ""
    echo "View logs: docker-compose logs -f"
    ;;
  2)
    echo ""
    echo "Starting in DEVELOPMENT mode (hot-reload)..."
    docker-compose -f docker-compose.dev.yml up --build
    ;;
  3)
    echo ""
    echo "Stopping all containers..."
    docker-compose down
    docker-compose -f docker-compose.dev.yml down
    echo "✅ All containers stopped"
    ;;
  4)
    echo ""
    echo "Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
    ;;
  5)
    echo ""
    echo "⚠️  WARNING: This will remove all containers, volumes, and cached data!"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
      echo ""
      echo "Cleaning everything..."
      docker-compose down -v
      docker-compose -f docker-compose.dev.yml down -v
      docker system prune -af --volumes
      echo "✅ Cleanup complete"
    fi
    ;;
  *)
    echo "Invalid option!"
    ;;
esac
