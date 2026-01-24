from fastapi import FastAPI, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "message": exc.detail
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later."
        },
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests",
            "message": "Rate limit exceeded. Please try again later."
        },
    )



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees", response_model=schemas.EmployeeResponse)
@limiter.limit("5/minute")
def add_employee(
    request: Request,
    data: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    if db.query(models.Employee).filter(
        (models.Employee.email == data.email) |
        (models.Employee.employee_id == data.employee_id)
    ).first():
        raise HTTPException(status_code=400, detail="Employee already exists")
    return crud.create_employee(db, data)

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
@limiter.limit("30/minute")
def list_employees(
    request: Request,
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
@limiter.limit("10/minute")
def remove_employee(
    request: Request,
    emp_id: int,
    db: Session = Depends(get_db)
):
    emp = crud.delete_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.post("/employees/{emp_id}/attendance")
@limiter.limit("20/minute")
def mark_att(
    request: Request,
    emp_id: int,
    data: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):
    return crud.mark_attendance(db, emp_id, data)

@app.get("/employees/{emp_id}/attendance")
def view_att(emp_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance(db, emp_id)
