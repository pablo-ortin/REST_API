import pandas as pd
from fastapi import  HTTPException
from db import SessionLocal


def read_html_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

presentation_html = read_html_file("presentation.html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_csv_data(filename):
    try:
        data = pd.read_csv(filename)
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")