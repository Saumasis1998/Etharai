from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees", response_model=schemas.EmployeeResponse)
def add_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(models.Employee).filter(
        (models.Employee.email == data.email) |
        (models.Employee.employee_id == data.employee_id)
    ).first():
        raise HTTPException(status_code=400, detail="Employee already exists")
    return crud.create_employee(db, data)

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

@app.delete("/employees/{emp_id}")
def remove_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = crud.delete_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.post("/employees/{emp_id}/attendance")
def mark_att(emp_id: int, data: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.mark_attendance(db, emp_id, data)

@app.get("/employees/{emp_id}/attendance")
def view_att(emp_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance(db, emp_id)
