"""
Setup Verification Script
Run this to verify your environment is correctly configured.
Usage: python verify_setup.py
"""
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.10 or higher"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Need 3.10+")
        return False

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} - Installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_postgres():
    """Check if PostgreSQL is accessible"""
    try:
        result = subprocess.run(
            ["psql", "--version"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ PostgreSQL - {version}")
            return True
        else:
            print("❌ PostgreSQL - Not accessible")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL - Command not found")
        return False

def check_database_connection():
    """Check if can connect to the database"""
    try:
        from app.core.config import settings
        from sqlalchemy import create_engine
        
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            print(f"✅ Database connection - OK")
            return True
    except Exception as e:
        print(f"❌ Database connection - Failed: {str(e)}")
        return False

def check_env_file():
    """Check if .env file exists"""
    import os
    if os.path.exists(".env"):
        print("✅ .env file - Found")
        return True
    else:
        print("❌ .env file - Not found (copy from .env.example)")
        return False

def main():
    print("=" * 50)
    print("ProfPulse Backend Setup Verification")
    print("=" * 50)
    print()
    
    checks = []
    
    print("1. Checking Python version...")
    checks.append(check_python_version())
    print()
    
    print("2. Checking environment file...")
    checks.append(check_env_file())
    print()
    
    print("3. Checking PostgreSQL...")
    checks.append(check_postgres())
    print()
    
    print("4. Checking Python packages...")
    packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "jose", "passlib"]
    for package in packages:
        checks.append(check_package(package))
    print()
    
    print("5. Checking database connection...")
    checks.append(check_database_connection())
    print()
    
    print("=" * 50)
    if all(checks):
        print("🎉 All checks passed! You're ready to start developing.")
        print()
        print("Next steps:")
        print("1. Run: uvicorn app.main:app --reload")
        print("2. Visit: http://localhost:8000/docs")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("Refer to README.md for setup instructions.")
    print("=" * 50)

if __name__ == "__main__":
    main()

