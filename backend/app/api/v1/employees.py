from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.common.rate_limiter import limiter
from app.domain.employee.service import EmployeeService
from app.domain.employee.repository import EmployeeRepository
from app.domain.employee.schemas import EmployeeCreate, EmployeeResponse
from fastapi import HTTPException
from typing import List

router = APIRouter()

@router.post("/employees", response_model=EmployeeResponse)
@limiter.limit("5/minute")
def create_employee(
    request: Request,
    data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(EmployeeRepository(db))
    return service.create_employee(data)


@router.get("/employees", response_model=List[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    service = EmployeeService(EmployeeRepository(db))
    return service.get_all_employees()


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(EmployeeRepository(db))
    emp = service.get_employee_by_id(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp
