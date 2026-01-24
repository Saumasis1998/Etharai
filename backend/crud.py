from sqlalchemy.orm import Session
from models import Employee, Attendance
from schemas import EmployeeCreate, AttendanceCreate


def create_employee(db: Session, data: EmployeeCreate):
    employee = Employee(**data.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employees(db: Session):
    return db.query(Employee).all()


def delete_employee(db: Session, emp_id: int):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if emp:
        db.delete(emp)
        db.commit()
    return emp


def mark_attendance(db: Session, emp_id: int, data: AttendanceCreate):
    attendance = Attendance(
        employee_id=emp_id,
        date=data.date,
        status=data.status
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def get_attendance(db: Session, emp_id: int):
    return db.query(Attendance).filter(
        Attendance.employee_id == emp_id
    ).all()
