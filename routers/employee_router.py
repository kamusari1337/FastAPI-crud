from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.employee_repository import EmployeeRepository
from schemas.employee_schemas import EmployeeIdSchema, EmployeeAddSchema, EmployeeUpdateSchema

router = APIRouter(tags=["Employee API"], prefix="/employee")


@router.post("/add/")
async def add_employee(employee: Annotated[EmployeeAddSchema, Depends()]):
    return await EmployeeRepository.add_employee(employee)


@router.get("/get/")
async def get_one_employee(employee: Annotated[EmployeeIdSchema, Depends()]):
    return await EmployeeRepository.get_employee(employee)


@router.get("/all/")
async def get_all_employees():
    return await EmployeeRepository.get_employees()


@router.put("/update/")
async def update_employee(employee: Annotated[EmployeeUpdateSchema, Depends()]):
    return await EmployeeRepository.update_employee(employee)


@router.delete("/delete/")
async def delete_employee(employee: Annotated[EmployeeIdSchema, Depends()]):
    return await EmployeeRepository.delete_employee(employee)
