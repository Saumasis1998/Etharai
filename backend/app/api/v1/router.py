from fastapi import APIRouter
from app.api.v1.employees import router as employee_router

api_router = APIRouter()
api_router.include_router(employee_router, tags=["Employees"])
