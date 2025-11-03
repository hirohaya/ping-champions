#!/bin/bash
# Pre-commit hook for Trunk-Based Development
# Install: cp scripts/pre-commit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -e

YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${YELLOW}🔍 Running pre-commit checks...${NC}"

# Check Python files
if [ -d "backend" ]; then
    echo -e "${YELLOW}  → Checking Python syntax...${NC}"
    
    # Get Python files that changed
    PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | grep backend/ || true)
    
    if [ ! -z "$PYTHON_FILES" ]; then
        echo "    Checking: $PYTHON_FILES"
        
        # Check syntax
        python -m py_compile $PYTHON_FILES 2>/dev/null || {
            echo -e "${RED}    ✗ Syntax error in Python files${NC}"
            exit 1
        }
        
        # Run black check (format only, don't modify)
        black --check $PYTHON_FILES 2>/dev/null || {
            echo -e "${YELLOW}    ⚠️  Code formatting issues found${NC}"
            echo "       Run: black backend/"
            echo "       Then: git add <files>"
        }
        
        # Run isort check
        isort --check-only $PYTHON_FILES 2>/dev/null || {
            echo -e "${YELLOW}    ⚠️  Import ordering issues found${NC}"
            echo "       Run: isort backend/"
            echo "       Then: git add <files>"
        }
        
        echo -e "${GREEN}    ✓ Python files OK${NC}"
    fi
fi

# Check frontend files
if [ -d "frontend" ]; then
    echo -e "${YELLOW}  → Checking JavaScript syntax...${NC}"
    
    JS_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|vue)$' | grep frontend/ || true)
    
    if [ ! -z "$JS_FILES" ]; then
        echo "    Checking: $JS_FILES"
        cd frontend 2>/dev/null && npm run lint 2>/dev/null || {
            echo -e "${YELLOW}    ⚠️  Linting issues found (non-blocking)${NC}"
        }
        cd - > /dev/null 2>&1
        echo -e "${GREEN}    ✓ JavaScript files OK${NC}"
    fi
fi

# Check commit message format
COMMIT_MSG_FILE=$1
if [ ! -z "$COMMIT_MSG_FILE" ]; then
    echo -e "${YELLOW}  → Checking commit message format...${NC}"
    
    # Read first line of commit message
    MSG=$(head -1 "$COMMIT_MSG_FILE" 2>/dev/null || echo "")
    
    # Pattern: type(scope): description
    if echo "$MSG" | grep -qE '^(feat|fix|refactor|perf|test|docs|style|chore|ci)(\(.+\))?!?: .+'; then
        # Check length <= 50 chars
        if [ ${#MSG} -le 50 ]; then
            echo -e "${GREEN}    ✓ Commit message format OK${NC}"
        else
            echo -e "${YELLOW}    ⚠️  First line > 50 characters (${#MSG})${NC}"
            echo "       Keep it concise!"
        fi
    else
        echo -e "${YELLOW}    ℹ️  Consider using Conventional Commits:${NC}"
        echo "       <type>(<scope>): <description>"
        echo "       Example: feat(events): add date filter"
        echo ""
        echo "       See: COMMIT_CONVENTIONS.md"
    fi
fi

echo -e "${GREEN}✅ Pre-commit checks passed!${NC}"
exit 0
