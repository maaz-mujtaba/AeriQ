# init_db.py
from app.database import engine, Base
from app.db_models import User

def init_database():
    print("📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("📁 Tables: users")

if __name__ == "__main__":
    init_database()