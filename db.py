from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# Database configuration
DATABASE_URL = "mysql://user:password@insert-your-database-name.abcdefgh.us-east-1.rds.amazonaws.com:3306/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

