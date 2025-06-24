#!/bin/bash
"""
Run the Hotel Chat Streamlit Application

This script launches the Streamlit web interface for the hotel chat application.
"""

echo "🏨 Starting Hotel Chat Streamlit Application..."
echo "🌐 The app will open in your browser at http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Run streamlit with custom configuration
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --theme.base "light" \
    --theme.primaryColor "#ff6b6b" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f0f2f6"
