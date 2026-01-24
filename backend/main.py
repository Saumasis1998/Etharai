from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://etharai-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def list_employees(
    db: Session = Depends(get_db),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(5, le=50),
):
    query = db.query(models.Employee)

    if search:
        query = query.filter(
            models.Employee.full_name.ilike(f"%{search}%") |
            models.Employee.email.ilike(f"%{search}%") |
            models.Employee.department.ilike(f"%{search}%")
        )

    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

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
