#!/bin/bash

# Stock/ETF Dashboard Launcher Script
echo "🚀 Starting Stock/ETF Dashboard..."

# Check if dashboard is already running
if pgrep -f "streamlit run main.py" > /dev/null; then
    echo "⚠️  Dashboard is already running!"
    echo "🌐 Access it at: http://localhost:8501"
    echo "🛑 To stop it, run: pkill -f 'streamlit run main.py'"
    exit 0
fi

# Navigate to app directory
cd "$(dirname "$0")/app"

# Start the dashboard
echo "📱 Starting dashboard on port 8501..."
python3 -m streamlit run main.py --server.port 8501 --server.headless true &

# Wait a moment for it to start
sleep 3

# Check if it's running
if pgrep -f "streamlit run main.py" > /dev/null; then
    echo "✅ Dashboard started successfully!"
    echo "🌐 Access it at: http://localhost:8501"
    echo "🛑 To stop it, run: pkill -f 'streamlit run main.py'"
else
    echo "❌ Failed to start dashboard"
    echo "💡 Make sure you're in the project directory and have Python dependencies installed"
fi
