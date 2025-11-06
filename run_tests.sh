#!/bin/bash
# Script to run the test suite for the badguys project

set -e

echo "=================================="
echo "Let's Be Bad Guys - Test Suite"
echo "=================================="
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not running in a virtual environment"
    echo "   It's recommended to activate your virtualenv first"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if pytest is installed
if ! python -c "import pytest" 2>/dev/null; then
    echo "📦 Installing test dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "🧪 Running tests..."
echo ""

# Run pytest with coverage
python -m pytest tests/ -v --cov=badguys --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests complete!"
echo ""
echo "📊 Coverage report saved to: htmlcov/index.html"
echo "   Open it in your browser to view detailed coverage information"

