"""
Seed Script - Populate database with test data
Run with: python seed_data.py
"""

from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.professor import Professor
from app.models.review import Review, GradeEnum
from app.core.security import hash_password
from datetime import datetime, timedelta
import random

# Sample data
PROFESSORS_DATA = [
    {"name": "Dr. Sarah Connor", "department": "Computer Science"},
    {"name": "Prof. John Smith", "department": "Mathematics"},
    {"name": "Dr. Alan Turing", "department": "Computer Science"},
    {"name": "Dr. Marie Curie", "department": "Physics"},
    {"name": "Prof. Albert Einstein", "department": "Physics"},
    {"name": "Dr. Ada Lovelace", "department": "Computer Science"},
    {"name": "Prof. Isaac Newton", "department": "Mathematics"},
    {"name": "Dr. Richard Feynman", "department": "Physics"},
]

COMMENTS = [
    "Amazing professor! Explains complex topics very clearly. Highly recommend!",
    "Tough grader but you'll learn a lot. Go to office hours!",
    "Very helpful and always available. The assignments are challenging but fair.",
    "Great lecturer, makes the subject interesting. Exams are straightforward.",
    "One of the best professors I've had. Really cares about students.",
    "Lectures can be dry but the material is important. Study the slides!",
    "Fair grading, clear expectations. Would take again.",
    "Challenging course but Professor is supportive. Attend every class!",
    "Excellent at breaking down difficult concepts. Homework helps a lot.",
    "Very knowledgeable and passionate about the subject.",
    "Clear grading rubric, no surprises. Midterm was tough but fair.",
    "Office hours are super helpful. Don't skip them!",
    "The textbook is optional - lectures cover everything you need.",
    "Group projects were actually useful. Good real-world applications.",
    "Strict about deadlines but understanding if you communicate early.",
]

COURSE_CODES = ["CS101", "CS201", "CS301", "MATH101", "MATH201", "PHYS101", "PHYS201", "CS401"]
SEMESTERS = ["Fall 2023", "Spring 2024", "Fall 2024"]

def seed_database():
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Check if data already exists
        existing_profs = db.query(Professor).count()
        if existing_profs > 0:
            print(f"⚠️  Database already has {existing_profs} professors. Skipping seed.")
            print("   To reseed, delete existing data first.")
            return
        
        # Create test users (students)
        print("\n📝 Creating test users...")
        users = []
        for i in range(1, 11):
            user = User(
                email=f"student{i}@university.edu",
                password_hash=hash_password("password123"),
                role=UserRole.STUDENT
            )
            db.add(user)
            users.append(user)
        
        # Create admin user
        admin = User(
            email="admin@university.edu",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        
        db.commit()
        print(f"   ✅ Created {len(users)} students + 1 admin")
        
        # Refresh users to get IDs
        for user in users:
            db.refresh(user)
        db.refresh(admin)
        
        # Create professors
        print("\n👨‍🏫 Creating professors...")
        professors = []
        for prof_data in PROFESSORS_DATA:
            professor = Professor(
                name=prof_data["name"],
                department=prof_data["department"],
                avg_rating=0.0,
                avg_difficulty=0.0,
                total_reviews=0
            )
            db.add(professor)
            professors.append(professor)
        
        db.commit()
        print(f"   ✅ Created {len(professors)} professors")
        
        # Refresh professors to get IDs
        for prof in professors:
            db.refresh(prof)
        
        # Create reviews
        print("\n⭐ Creating reviews...")
        review_count = 0
        
        for professor in professors:
            # Each professor gets 5-15 random reviews
            num_reviews = random.randint(5, 15)
            
            # Randomly select students for this professor
            reviewers = random.sample(users, min(num_reviews, len(users)))
            
            for i, student in enumerate(reviewers):
                # Randomize ratings with some bias based on professor
                base_quality = random.uniform(3.0, 5.0)
                base_difficulty = random.uniform(2.0, 4.5)
                
                review = Review(
                    professor_id=professor.id,
                    student_id=student.id,
                    rating_quality=min(5, max(1, int(base_quality + random.uniform(-1, 1)))),
                    rating_difficulty=min(5, max(1, int(base_difficulty + random.uniform(-1, 1)))),
                    grade_received=random.choice(list(GradeEnum)),
                    comment=random.choice(COMMENTS),
                    course_code=random.choice(COURSE_CODES),
                    semester=SEMESTERS[i % len(SEMESTERS)],
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
                )
                db.add(review)
                review_count += 1
        
        db.commit()
        print(f"   ✅ Created {review_count} reviews")
        
        # Update professor aggregate stats
        print("\n📊 Updating professor statistics...")
        for professor in professors:
            reviews = db.query(Review).filter(Review.professor_id == professor.id).all()
            if reviews:
                professor.avg_rating = sum(r.rating_quality for r in reviews) / len(reviews)
                professor.avg_difficulty = sum(r.rating_difficulty for r in reviews) / len(reviews)
                professor.total_reviews = len(reviews)
        
        db.commit()
        print("   ✅ Statistics updated")
        
        # Print summary
        print("\n" + "="*50)
        print("🎉 SEEDING COMPLETE!")
        print("="*50)
        print(f"\n📋 Summary:")
        print(f"   • Students: 10 (student1@university.edu ... student10@university.edu)")
        print(f"   • Admin: admin@university.edu (password: admin123)")
        print(f"   • Professors: {len(professors)}")
        print(f"   • Reviews: {review_count}")
        print(f"\n🔑 Test credentials:")
        print(f"   • Student: student1@university.edu / password123")
        print(f"   • Admin: admin@university.edu / admin123")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

