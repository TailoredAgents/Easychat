#!/usr/bin/env python3
"""
Setup script for Universal Chat + Doc QA Web App
This script helps users set up their environment quickly
"""

import os
import sys
import subprocess

def create_env_file():
    """Create .env file with template values"""
    env_content = """# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Model Selection (choose one)
MODEL_NAME=gpt-4o        # Highest quality (more expensive)
# MODEL_NAME=gpt-4o-mini  # Faster & cheaper alternative

# Optional: Set environment to production
# ENVIRONMENT=production
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your OpenAI API key!")
    else:
        print("⚠️  .env file already exists")

def install_dependencies():
    """Install required Python packages"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def main():
    print("🚀 Setting up Universal Chat + Doc QA Web App...")
    print()
    
    # Create environment file
    create_env_file()
    print()
    
    # Install dependencies
    if install_dependencies():
        print()
        print("🎉 Setup complete!")
        print()
        print("Next steps:")
        print("1. Edit .env and add your OpenAI API key")
        print("2. Run: streamlit run app.py")
        print("3. Open http://localhost:8501")
        print("4. Login with: admin/admin123 or user/user123")
        print()
        print("Happy chatting! 🤖")
    else:
        print("❌ Setup failed. Please check error messages above.")

if __name__ == "__main__":
    main() 