from sqlalchemy.inspection import inspect
from db import engine
from models import Base
from sqlalchemy.orm import Session
from fastapi import  Depends
from tools import get_db, read_csv_data
from models import Department, Employee, Job
import os
from sqlalchemy.orm import sessionmaker


def create_tables(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    
    required_tables = {"department", "job", "employee"}
    missing_tables = required_tables - existing_tables
    
    if not missing_tables:
        return {"message": "Tables already exist in the database"}
    
    Base.metadata.create_all(bind=engine)
    return {"message": "Tables created"}


def ingest_data():
    try:
        tables_and_csv = [
            (Department, "department.csv"),
            (Employee, "employee.csv"),
            (Job, "job.csv")
        ]
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        for model, csv_filename in tables_and_csv:
            csv_path = os.path.join(os.path.dirname(__file__), "uploads", csv_filename)
            data = read_csv_data(csv_path)
            
            with SessionLocal() as db:
                for row in data:
                    db_instance = model(**row)
                    db.add(db_instance)
                db.commit()
        
        return {"message": "Data ingested successfully"}
    except Exception as e:
        return {"error": str(e)}