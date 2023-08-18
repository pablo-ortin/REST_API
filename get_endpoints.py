from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import func
from db import SessionLocal
from models import Department, Employee, Job


def get_employees_by_quarter():
    session = SessionLocal()

    q1_case = text("CASE WHEN employee.datetime BETWEEN '2021-01-01' AND '2021-03-31' THEN 1 ELSE 0 END")
    q2_case = text("CASE WHEN employee.datetime BETWEEN '2021-04-01' AND '2021-06-30' THEN 1 ELSE 0 END")
    q3_case = text("CASE WHEN employee.datetime BETWEEN '2021-07-01' AND '2021-09-30' THEN 1 ELSE 0 END")
    q4_case = text("CASE WHEN employee.datetime BETWEEN '2021-10-01' AND '2021-12-31' THEN 1 ELSE 0 END")

    query = (session
             .query(Department.department, Job.job,
                    func.sum(q1_case).label('Q1'),
                    func.sum(q2_case).label('Q2'),
                    func.sum(q3_case).label('Q3'),
                    func.sum(q4_case).label('Q4'))
             .join(Employee, Department.id == Employee.department_id)
             .join(Job, Job.id == Employee.job_id)
             .filter(Employee.datetime.between('2021-01-01', '2021-12-31'))
             .group_by(Department.department, Job.job)
             .order_by(Department.department, Job.job))

    results = []
    for row in query:
        results.append({
            "department": row.department,
            "job": row.job,
            "Q1": row.Q1,
            "Q2": row.Q2,
            "Q3": row.Q3,
            "Q4": row.Q4
        })

    session.close()
    
    return results

def get_departments_above_average():
    session = SessionLocal()

    subquery = (session
                .query(Employee.department_id, func.count(Employee.id).label('dept_employee_count'))
                .filter(Employee.datetime.between('2021-01-01', '2021-12-31'))
                .group_by(Employee.department_id)
                .subquery())

    avg_query = (session
                 .query(func.avg(subquery.c.dept_employee_count))
                 .scalar_subquery())

    query = (session
             .query(Department.id, Department.department, func.count(Employee.id).label('hired'))
             .join(Employee, Department.id == Employee.department_id)
             .filter(Employee.datetime.between('2021-01-01', '2021-12-31'))
             .group_by(Department.id, Department.department)
             .having(func.count(Employee.id) > avg_query)
             .order_by(func.count(Employee.id).desc()))

    results = []
    for row in query:
        results.append({
            "id": row.id,
            "department": row.department,
            "hired": row.hired
        })

    session.close()
    return results