#!/usr/bin/env python3
"""
Simple startup script for the Stock/ETF Dashboard
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Stock/ETF Dashboard...")
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: Please run this from the project root directory")
        print("   Current directory:", os.getcwd())
        sys.exit(1)
    
    # Change to app directory and start
    os.chdir("app")
    print("✅ Starting dashboard on http://localhost:8501")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
