#!/usr/bin/env python3
"""
Quick start script for AI-Powered Face Matching System
"""
import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def create_directories():
    """Create necessary directories"""
    dirs = ["uploads", "database", "static/css", "static/js", "static/images", "templates"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created necessary directories")


def setup_env():
    """Setup environment file"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from .env.example")
        else:
            print("⚠️  .env.example not found, skipping .env creation")
    else:
        print("✅ .env file already exists")


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    print("   This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies")
        print("   Please install manually: pip install -r requirements.txt")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 AI-Powered Face Matching System - Quick Setup")
    print("=" * 60)
    print()
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_env()
    
    # Ask user if they want to install dependencies
    print("\n" + "=" * 60)
    response = input("📦 Install dependencies now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        if install_dependencies():
            print("\n" + "=" * 60)
            print("✅ Setup completed successfully!")
            print("=" * 60)
            print("\n📝 Next steps:")
            print("   1. Edit .env file if needed")
            print("   2. Run: python main.py")
            print("   3. Open: http://localhost:8000")
            print("\n💡 For detailed instructions, see SETUP_GUIDE.md")
            print()
        else:
            print("\n⚠️  Please install dependencies manually and then run: python main.py")
    else:
        print("\n⚠️  Skipped dependency installation")
        print("   Please run: pip install -r requirements.txt")
        print("   Then run: python main.py")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
