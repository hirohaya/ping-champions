#!/bin/bash
# Quick development commands for Trunk-Based Development

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

case "$1" in
    backend)
        echo -e "${BLUE}Starting backend server...${NC}"
        cd backend
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
        uvicorn main:app --reload
        ;;
    
    frontend)
        echo -e "${BLUE}Starting frontend dev server...${NC}"
        cd frontend
        npm run dev
        ;;
    
    lint-backend)
        echo -e "${BLUE}Linting backend code...${NC}"
        cd backend
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
        flake8 . --statistics
        black . --check
        isort . --check-only
        ;;
    
    format-backend)
        echo -e "${BLUE}Formatting backend code...${NC}"
        cd backend
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
        black .
        isort .
        ;;
    
    lint-frontend)
        echo -e "${BLUE}Linting frontend code...${NC}"
        cd frontend
        npm run lint
        ;;
    
    test-backend)
        echo -e "${BLUE}Running backend tests...${NC}"
        cd backend
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
        pytest
        ;;
    
    test-frontend)
        echo -e "${BLUE}Running frontend tests...${NC}"
        cd frontend
        npm run test
        ;;
    
    build-frontend)
        echo -e "${BLUE}Building frontend...${NC}"
        cd frontend
        npm run build
        ;;
    
    sync)
        echo -e "${BLUE}Syncing with main branch...${NC}"
        git checkout main
        git pull origin main --rebase
        ;;
    
    status)
        echo -e "${BLUE}Repository status:${NC}"
        echo ""
        echo "Current branch:"
        git branch -v
        echo ""
        echo "Latest commits:"
        git log --oneline -5
        echo ""
        echo "Local changes:"
        git status --short
        ;;
    
    *)
        echo -e "${BLUE}Ping Champions Development Commands${NC}"
        echo ""
        echo "Usage: source scripts/dev.sh <command>"
        echo ""
        echo "Commands:"
        echo "  ${GREEN}backend${NC}              Start backend server (uvicorn)"
        echo "  ${GREEN}frontend${NC}             Start frontend dev server (npm run dev)"
        echo "  ${GREEN}lint-backend${NC}         Run flake8, black, isort checks"
        echo "  ${GREEN}format-backend${NC}       Format backend code with black/isort"
        echo "  ${GREEN}lint-frontend${NC}        Run ESLint on frontend"
        echo "  ${GREEN}test-backend${NC}         Run pytest"
        echo "  ${GREEN}test-frontend${NC}        Run frontend tests"
        echo "  ${GREEN}build-frontend${NC}       Build frontend for production"
        echo "  ${GREEN}sync${NC}                 Sync local main with origin"
        echo "  ${GREEN}status${NC}               Show repo and changes status"
        echo ""
        echo "Example:"
        echo "  source scripts/dev.sh backend"
        echo "  source scripts/dev.sh lint-backend"
        ;;
esac
