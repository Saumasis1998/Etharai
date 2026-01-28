from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    department = Column(String, nullable=False)
