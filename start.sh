#!/bin/bash

echo "🎯 Starting ContentEngine..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements if needed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Launch the application
echo "🚀 Launching ContentEngine at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo "================================"

cd frontend
streamlit run app.py --server.port=8501 --browser.gatherUsageStats=false --server.headless=true