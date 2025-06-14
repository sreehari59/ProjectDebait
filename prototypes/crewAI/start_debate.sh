#!/bin/bash

# Quick start script for the AI Debate System
echo "🎭 AI Debate System - Quick Start"
echo "================================="
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source debate_env/bin/activate

# Check if topic is provided as argument
if [ $# -eq 0 ]; then
    echo "💭 Enter your debate topic:"
    read -p "Topic: " topic
    python debate_system.py "$topic"
else
    python debate_system.py "$@"
fi
