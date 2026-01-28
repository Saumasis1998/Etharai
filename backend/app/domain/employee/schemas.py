from pydantic import BaseModel, EmailStr
from datetime import date
from pydantic import ConfigDict


class EmployeeCreate(BaseModel):
	employee_id: str
	full_name: str
	email: EmailStr
	department: str


class EmployeeResponse(EmployeeCreate):
	id: int
	model_config = ConfigDict(from_attributes=True)


class AttendanceCreate(BaseModel):
	date: date
	status: str


class AttendanceResponse(AttendanceCreate):
	id: int
	model_config = ConfigDict(from_attributes=True)

__all__ = ["EmployeeCreate", "EmployeeResponse", "AttendanceCreate", "AttendanceResponse"]
