from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the base for declaring models

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String(length=100))

class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String(length=100))

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    datetime = Column(DateTime)
    department_id = Column(Integer)
    job_id = Column(Integer)



