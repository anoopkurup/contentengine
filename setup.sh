#!/bin/bash

# ContentEngine Setup Script

echo "🚀 Setting up ContentEngine environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "ContentEngine-env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv ContentEngine-env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ContentEngine-env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API credentials!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials:"
echo "   - DATAFORSEO_LOGIN=your_email@example.com"
echo "   - DATAFORSEO_PASSWORD=your_api_password"
echo "   - OPENAI_API_KEY=sk-your_openai_key"
echo ""
echo "2. To activate the environment in future sessions:"
echo "   source ContentEngine-env/bin/activate"
echo ""
echo "3. Run the content pipeline:"
echo "   python KeywordResearcher.py"
echo "   python ArticleBrief.py"
echo "   python ArticleWriter.py"
echo "   python SocialMedia.py"
echo "   python YoutTubeScript.py"