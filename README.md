# ProfPulse - Professor Review Platform

A data-driven academic feedback platform where students can review professors and visualize grading trends through interactive charts.

## 🎯 Core Features

- **Professor Profiles**: Aggregate stats (Difficulty, Quality) with Grade Distribution charts
- **Review System**: Students post reviews with tags and specific grades received
- **Role-Based Access**: Students, Professors, and Admins with different permissions
- **Data Visualization**: Grade distribution charts using student-reported grades

## 🛠 Tech Stack

- **Backend**: FastAPI (Python), SQLAlchemy ORM, Pydantic validation
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend** (Coming soon): React (Vite), Tailwind CSS, Recharts

---

## 📦 Backend Setup Instructions

### Prerequisites

Ensure you have the following installed:

1. **Python 3.10+**
   ```bash
   python --version  # Should show 3.10 or higher
   ```

2. **PostgreSQL 14+**
   - **Mac**: `brew install postgresql@14` or download Postgres.app
   - **Windows**: Download from postgresql.org
   ```bash
   psql --version  # Should show PostgreSQL 14+
   ```

3. **pip** (Python package manager - comes with Python)

---

### Step 1: Database Setup

1. **Start PostgreSQL** (if not already running)
   ```bash
   # Mac (if using brew)
   brew services start postgresql@14
   
   # Or check if it's running
   pg_isready
   ```

2. **Create the database and user**
   ```bash
   psql postgres
   ```
   
   Then run these SQL commands:
   ```sql
   CREATE DATABASE profpulse_db;
   CREATE USER profpulse_user WITH PASSWORD 'dev_password_123';
   GRANT ALL PRIVILEGES ON DATABASE profpulse_db TO profpulse_user;
   \q
   ```

3. **Verify the connection**
   ```bash
   psql -U profpulse_user -d profpulse_db -h localhost
   # Enter password: dev_password_123
   # You should see the database prompt
   \q
   ```

---

### Step 2: Python Environment Setup

1. **Navigate to the server directory**
   ```bash
   cd server
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```
   
   **Why?** Virtual environments isolate project dependencies so they don't conflict with other Python projects.

3. **Activate the virtual environment**
   ```bash
   # Mac/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```
   
   You should see `(venv)` appear in your terminal prompt.

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - FastAPI: Web framework
   - Uvicorn: ASGI server to run FastAPI
   - SQLAlchemy: Database ORM
   - Psycopg2: PostgreSQL adapter
   - Pydantic: Data validation
   - Python-Jose: JWT token handling
   - Passlib: Password hashing
   - Alembic: Database migrations

---

### Step 3: Environment Configuration

The `.env` file has been created with default development settings. **DO NOT commit this file to Git** (it's already in `.gitignore`).

**Contents of `.env`** (already created):
```
DATABASE_URL=postgresql://profpulse_user:dev_password_123@localhost/profpulse_db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ Security Note**: Before deploying to production, generate a new SECRET_KEY:
```bash
openssl rand -hex 32
```

---

### Step 4: Run the Application

1. **Start the FastAPI server**
   ```bash
   # Make sure you're in the server directory with venv activated
   uvicorn app.main:app --reload
   ```
   
   **Flags explained**:
   - `app.main:app` → Look for the `app` object in `app/main.py`
   - `--reload` → Auto-restart when code changes (development only)

2. **Verify it's running**
   
   Open your browser and visit:
   - http://localhost:8000 → Should show `{"message": "ProfPulse API is running"}`
   - http://localhost:8000/docs → FastAPI's **interactive API documentation** (very useful!)
   - http://localhost:8000/redoc → Alternative API documentation

---

## 📁 Project Structure

```
server/
├── app/
│   ├── core/              # Core configuration
│   │   ├── config.py      # Environment variables and settings
│   │   └── database.py    # Database connection setup
│   ├── models/            # SQLAlchemy database models
│   │   └── (your models here: user.py, professor.py, review.py)
│   ├── schemas/           # Pydantic validation schemas
│   │   └── (your schemas here: user.py, professor.py, review.py)
│   ├── routers/           # API endpoint routes
│   │   └── (your routers here: auth.py, professors.py, reviews.py)
│   └── main.py            # FastAPI application entry point
├── alembic/               # Database migrations (to be set up)
├── venv/                  # Virtual environment (not committed to Git)
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not committed to Git)
```

---

## 🚀 Development Workflow

### Creating a New Feature

1. **Create the database model** in `app/models/`
2. **Create Pydantic schemas** in `app/schemas/`
3. **Create API routes** in `app/routers/`
4. **Register the router** in `app/main.py`
5. **Test using the `/docs` endpoint**

### Example: Adding a Router

```python
# In app/main.py
from app.routers import auth, professors

app.include_router(auth.router)
app.include_router(professors.router)
```

---

## 🧪 Testing Your API

FastAPI provides an **automatic interactive API documentation** at http://localhost:8000/docs

You can:
- See all your endpoints
- Try them directly in the browser
- View request/response schemas
- Test authentication

**Alternative tools**:
- **Postman**: GUI for testing APIs
- **curl**: Command-line HTTP client
  ```bash
  curl http://localhost:8000/
  ```

---

## 🗄 Database Migrations with Alembic

Once you create your models, you'll need to set up Alembic for database migrations.

### Initialize Alembic (Do this once)

```bash
# In the server directory
alembic init alembic
```

### Configure Alembic

Edit `alembic/env.py` to import your models and use your database URL.

### Create a Migration

```bash
alembic revision --autogenerate -m "Create users table"
```

### Apply Migration

```bash
alembic upgrade head
```

---

## 📚 Resources for Learning

### FastAPI
- [Official Tutorial](https://fastapi.tiangolo.com/tutorial/) - Best starting point
- [SQL Databases Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### SQLAlchemy
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)

### Pydantic
- [Pydantic Documentation](https://docs.pydantic.dev/latest/)

### PostgreSQL
- Use **TablePlus** or **pgAdmin** to view your database visually

---

## 🐛 Common Issues & Solutions

### Issue: "Can't connect to database"
**Solution**: 
- Check if PostgreSQL is running: `pg_isready`
- Verify credentials in `.env` match what you created
- Check if the database exists: `psql -l`

### Issue: "Module not found"
**Solution**: 
- Make sure virtual environment is activated (you see `(venv)`)
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: "Port 8000 already in use"
**Solution**: 
- Either stop the other process using port 8000
- Or use a different port: `uvicorn app.main:app --reload --port 8001`

### Issue: "Import errors in Python files"
**Solution**: 
- Make sure you're running from the `server` directory
- Check that `__init__.py` files exist in all folders

---

## 👥 Team Collaboration

### Git Workflow

```bash
# Before starting work
git pull origin dev

# Create a feature branch
git checkout -b feature/your-name-feature-description

# After making changes
git add .
git commit -m "feat: descriptive message"
git push origin feature/your-name-feature-description

# Create Pull Request on GitHub
```

### Daily Standup Questions
1. What did I complete yesterday?
2. What am I working on today?
3. Am I blocked on anything?

---

## 🎓 Next Steps

Follow the **ProfPulse Development Roadmap** document to build features in this order:

1. **Phase 1**: Authentication (Users, Login, JWT)
2. **Phase 2**: Professor Profiles (CRUD operations)
3. **Phase 3**: Review System (with grade input)
4. **Phase 4**: Grade Distribution Visualization (core feature)
5. **Phase 5**: Search & Admin features
6. **Phase 6**: Testing & Deployment

Good luck building ProfPulse! 🚀

