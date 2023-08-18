from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from tools import get_db, presentation_html
from post_endpoints import create_tables, ingest_data
from get_endpoints import get_employees_by_quarter, get_departments_above_average
from starlette.responses import  HTMLResponse

# App
app = FastAPI(
    title='Employee API')

# Presentation

@app.get("/", response_class=HTMLResponse)
def main():
    return presentation_html


# Endpoint #1 Table Creation

@app.post("/create_tables/")
async def create_database_tables(db: Session = Depends(get_db)):
    return create_tables(db) 

# Endpoint #2 Uploading the data 

@app.post("/ingest_data/")
def ingest():
    return ingest_data()

# Endpoint #3 Get employees hired by quarter

@app.get("/employees-by-quarter")
async def employees_by_quarter():
    return get_employees_by_quarter()

# Endpoint #4 Get departments above average

@app.get("/departments-above-average")
async def departments_above_average():
    return get_departments_above_average()
    
