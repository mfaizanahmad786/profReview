"""
Script to create an admin user
Run: python create_admin.py
"""
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(
            User.email == 'admin@university.com'
        ).first()
        
        if existing_admin:
            print('⚠️  Admin user already exists!')
            print('Email: admin@test.com')
            print('If you forgot the password, delete this user from the database first.')
            return
        
        # Create new admin user
        admin = User(
            email='admin@university.com',
            password_hash=hash_password('admin123'),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        
        print('✅ Admin user created successfully!')
        print('=' * 50)
        print('Email: admin@test.com')
        print('Password: admin123')
        print('=' * 50)
        print('\n📝 You can now login with these credentials')
        
    except Exception as e:
        print(f'❌ Error creating admin: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    create_admin()
