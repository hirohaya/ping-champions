#!/usr/bin/env python
"""
Unified setup and initialization script for Ping Champions project.
Handles backend, frontend, and database setup in one place.
"""

import sys
import os
import subprocess
import platform
from pathlib import Path
from typing import Optional

# Color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def disable():
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')


# Disable colors on Windows CMD
if platform.system() == 'Windows' and not os.getenv('TERM'):
    Colors.disable()


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}\n")


def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}[OK]{Colors.END} {message}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}[ERROR]{Colors.END} {message}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {message}")


def print_info(message: str):
    """Print an info message"""
    print(f"{Colors.BLUE}[INFO]{Colors.END} {message}")


def run_command(command, cwd: Optional[str] = None, check: bool = True) -> bool:
    """Execute a command and return success status"""
    try:
        use_shell = isinstance(command, str) or platform.system() == 'Windows'
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=False,
            text=True,
            check=False,
            shell=use_shell
        )
        return result.returncode == 0
    except Exception as e:
        print_error(f"Failed to run command: {e}")
        return False


def setup_backend():
    """Setup backend environment and dependencies"""
    print_section("Backend Setup")
    
    backend_path = Path("backend")
    
    # Check Python version
    print_info(f"Python version: {sys.version.split()[0]}")
    
    # Create venv if needed
    venv_path = backend_path / "venv"
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", "backend/venv"]):
            print_error("Failed to create virtual environment")
            return False
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment exists")
    
    # Install dependencies using python -m pip
    print_info("Installing backend dependencies...")
    req_file = backend_path / "requirements.txt"
    if req_file.exists():
        if platform.system() == 'Windows':
            python_exe = "backend\\venv\\Scripts\\python.exe"
        else:
            python_exe = "backend/venv/bin/python"
        
        if not run_command(f'"{python_exe}" -m pip install -r backend/requirements.txt'):
            print_error("Failed to install requirements")
            return False
        print_success("Requirements installed")
    
    # Install dev dependencies
    req_dev_file = backend_path / "requirements-dev.txt"
    if req_dev_file.exists():
        if platform.system() == 'Windows':
            python_exe = "backend\\venv\\Scripts\\python.exe"
        else:
            python_exe = "backend/venv/bin/python"
            
        if not run_command(f'"{python_exe}" -m pip install -r backend/requirements-dev.txt'):
            print_warning("Failed to install dev requirements (optional)")
        else:
            print_success("Dev requirements installed")
    
    return True


def setup_frontend():
    """Setup frontend environment and dependencies"""
    print_section("Frontend Setup")
    
    frontend_path = Path("frontend")
    
    # Check Node.js
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print_success(f"Node.js {result.stdout.strip()} found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Node.js is not installed")
        print_info("Please install Node.js 18+ from https://nodejs.org/")
        return False
    
    # Install npm dependencies
    print_info("Installing frontend dependencies...")
    if not run_command(
        ["npm", "ci"] if (frontend_path / "node_modules").exists() else ["npm", "install"],
        cwd=str(frontend_path)
    ):
        print_error("Failed to install frontend dependencies")
        return False
    print_success("Frontend dependencies installed")
    
    return True


def setup_database():
    """Setup and initialize database"""
    print_section("Database Setup")
    
    db_script = Path("recreate_db.py")
    if not db_script.exists():
        print_warning("Database recreation script not found")
        return True  # Don't fail if script not found
    
    print_info("Recreating database with fresh schema...")
    if not run_command([sys.executable, str(db_script)]):
        print_error("Failed to setup database")
        return False
    print_success("Database initialized")
    
    return True


def create_env_files():
    """Create environment files if they don't exist"""
    print_section("Environment Configuration")
    
    # Backend .env
    backend_env = Path("backend") / ".env"
    if not backend_env.exists():
        print_info("Creating backend .env file...")
        backend_env.write_text(
            "# Backend Configuration\n"
            "DATABASE_URL=sqlite:///./pingchampions.db\n"
            "DEBUG=True\n"
            'CORS_ORIGINS=["http://localhost:5173"]\n'
        )
        print_success("Backend .env created")
    else:
        print_success("Backend .env exists")
    
    # Frontend .env.local
    frontend_env = Path("frontend") / ".env.local"
    if not frontend_env.exists():
        print_info("Creating frontend .env.local file...")
        frontend_env.write_text(
            "# Frontend Configuration\n"
            "VITE_API_BASE_URL=http://localhost:8000\n"
            "VITE_DEBUG=true\n"
        )
        print_success("Frontend .env.local created")
    else:
        print_success("Frontend .env.local exists")
    
    return True


def show_next_steps():
    """Display next steps to run the project"""
    print_section("Setup Complete!")
    
    print(f"{Colors.GREEN}{Colors.BOLD}[OK] All components configured successfully!{Colors.END}\n")
    
    if platform.system() == 'Windows':
        print(f"{Colors.BOLD}Next steps:{Colors.END}\n")
        print("1. Start backend server:")
        print(f"   {Colors.YELLOW}python run_backend.py{Colors.END}\n")
        print("2. Start frontend dev server (in another terminal):")
        print(f"   {Colors.YELLOW}cd frontend && npm run dev{Colors.END}\n")
    else:
        print(f"{Colors.BOLD}Next steps:{Colors.END}\n")
        print("1. Start backend server:")
        print(f"   {Colors.YELLOW}python run_backend.py{Colors.END}\n")
        print("2. Start frontend dev server (in another terminal):")
        print(f"   {Colors.YELLOW}cd frontend && npm run dev{Colors.END}\n")
    
    print(f"{Colors.BOLD}URLs:{Colors.END}")
    print(f"  - API: {Colors.YELLOW}http://127.0.0.1:8000{Colors.END}")
    print(f"  - Frontend: {Colors.YELLOW}http://localhost:5173{Colors.END}")
    print(f"  - API Docs: {Colors.YELLOW}http://127.0.0.1:8000/docs{Colors.END}\n")


def main():
    """Main setup orchestration"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("  ================================")
    print("  Ping Champions - Setup")
    print("  ================================")
    print(f"{Colors.END}\n")
    
    # Ensure we're in the project root
    if not Path("backend").exists() or not Path("frontend").exists():
        print_error("Please run this script from the project root directory")
        sys.exit(1)
    
    try:
        # Run setup steps
        steps = [
            ("Backend", setup_backend),
            ("Frontend", setup_frontend),
            ("Environment Files", create_env_files),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print_error(f"{step_name} setup failed")
                sys.exit(1)
        
        # Show completion message
        show_next_steps()
        
    except KeyboardInterrupt:
        print_error("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
