from app.domain.employee.repository import EmployeeRepository
from app.domain.employee.models import Employee

class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def create_employee(self, data):
        employee = Employee(**data.dict())
        return self.repo.create(employee)
