from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.common.rate_limiter import limiter
from app.domain.employee.service import EmployeeService
from app.domain.employee.repository import EmployeeRepository
from app.domain.employee.schemas import EmployeeCreate

router = APIRouter()

@router.post("/employees")
@limiter.limit("5/minute")
def create_employee(
    request: Request,
    data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    service = EmployeeService(EmployeeRepository(db))
    return service.create_employee(data)
