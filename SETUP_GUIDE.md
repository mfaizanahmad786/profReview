# Quick Setup Guide for Team Members

This guide will help you get the ProfPulse backend running on your machine.

## Step-by-Step Setup (15 minutes)

### 1️⃣ Install Required Software

**Install Python 3.10+**
- Mac: `brew install python@3.10` or download from python.org
- Windows: Download from python.org
- Verify: `python --version`

**Install PostgreSQL 14+**
- Mac: `brew install postgresql@14` or download Postgres.app
- Windows: Download from postgresql.org
- Verify: `psql --version`

### 2️⃣ Set Up the Database

Open terminal and run:

```bash
# Start PostgreSQL (Mac with brew)
brew services start postgresql@14

# Create database
psql postgres
```

In the PostgreSQL prompt, run:
```sql
CREATE DATABASE profpulse_db;
CREATE USER profpulse_user WITH PASSWORD 'dev_password_123';
GRANT ALL PRIVILEGES ON DATABASE profpulse_db TO profpulse_user;
\q
```

### 3️⃣ Set Up Python Environment

```bash
# Navigate to project
cd /path/to/Web\ Final/server

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4️⃣ Verify Setup

```bash
# Run verification script
python verify_setup.py
```

If all checks pass ✅, you're ready!

### 5️⃣ Start the Server

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the API documentation.

---

## Common Problems

### "venv not activating"
- **Mac/Linux**: Make sure you use `source venv/bin/activate`
- **Windows**: Use `venv\Scripts\activate`
- You should see `(venv)` in your terminal

### "Can't connect to database"
1. Check PostgreSQL is running: `pg_isready`
2. Verify database exists: `psql -l | grep profpulse`
3. Test connection: `psql -U profpulse_user -d profpulse_db -h localhost`

### "Module not found errors"
- Activate virtual environment first
- Then: `pip install -r requirements.txt`

---

## Daily Workflow

Every time you work on the project:

```bash
# 1. Navigate to server folder
cd server

# 2. Activate virtual environment
source venv/bin/activate

# 3. Pull latest changes
git pull origin dev

# 4. Start server
uvicorn app.main:app --reload
```

---

## Need Help?

1. Check the main **README.md** for detailed explanations
2. Ask in your team group chat
3. Check http://localhost:8000/docs for API testing

