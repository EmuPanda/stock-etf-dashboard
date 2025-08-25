#!/usr/bin/env python3
"""
Launcher script for the Stock/ETF Dashboard
Run this to start the dashboard with the new modular structure
"""

import streamlit.web.cli as stcli
import sys
import os

if __name__ == '__main__':
    # Set the working directory to the app folder
    app_dir = os.path.join(os.path.dirname(__file__), 'app')
    
    # Change to app directory
    os.chdir(app_dir)
    
    # Set up sys.argv for streamlit
    sys.argv = [
        "streamlit", "run", "main.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ]
    
    # Run streamlit
    sys.exit(stcli.main())
