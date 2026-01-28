from sqlalchemy.orm import Session
from app.domain.employee.models import Employee

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Employee).all()

    def create(self, employee: Employee):
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
