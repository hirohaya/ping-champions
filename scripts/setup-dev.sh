#!/bin/bash
# Development environment setup script for Trunk-Based Development

set -e  # Exit on error

echo "🚀 Setting up Ping Champions development environment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Setup
echo -e "${BLUE}=== Backend Setup ===${NC}"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -f "venv/Scripts/activate" ]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Mac
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing backend dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# Backend Configuration
DATABASE_URL=sqlite:///./pingchampions.db
DEBUG=True
CORS_ORIGINS=["http://localhost:5173"]
EOF
    echo "   Note: Edit .env with your configuration"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Frontend Setup
echo -e "${BLUE}=== Frontend Setup ===${NC}"

cd ../frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js is not installed${NC}"
    echo "   Please install Node.js 18+ from https://nodejs.org/"
else
    NODE_VERSION=$(node -v)
    echo "✓ Node.js $NODE_VERSION found"
fi

# Install dependencies
if [ -d "node_modules" ]; then
    echo "✓ Dependencies exist, running npm ci..."
    npm ci
else
    echo "📥 Installing frontend dependencies..."
    npm install
fi

# Create .env if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local file..."
    cat > .env.local << 'EOF'
# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_DEBUG=true
EOF
    echo "   Note: Edit .env.local with your configuration"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Return to root
cd ..

# Final setup
echo -e "${BLUE}=== Final Setup ===${NC}"

# Create directories if they don't exist
mkdir -p .git/hooks

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Start backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # or: source venv/Scripts/activate (Windows)"
echo "   uvicorn main:app --reload"
echo ""
echo "2. Start frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Read the guides:"
echo "   - TRUNK_BASED_DEV_GUIDE.md"
echo "   - COMMIT_CONVENTIONS.md"
echo ""
