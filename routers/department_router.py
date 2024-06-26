from typing import Annotated

from fastapi import APIRouter, Depends
from repositories.department_repository import DepartmentRepository
from schemas.department_schemas import (
    DepartmentNameSchema, DepartmentUpdateSchema)

router = APIRouter(tags=["Department API"], prefix="/department")


@router.post("/add/")
async def add_department(department: Annotated[DepartmentNameSchema, Depends()]):
    return await DepartmentRepository.add_department(department)


@router.get("/get/")
async def get_one_department(department: Annotated[DepartmentNameSchema, Depends()]):
    return await DepartmentRepository.get_department(department)


@router.get("/all/")
async def get_all_departments():
    return await DepartmentRepository.get_departments()


@router.put("/update/")
async def update_department(department: Annotated[DepartmentUpdateSchema, Depends()]):
    return await DepartmentRepository.update_department(department)


@router.delete("/delete/")
async def delete_department(department: Annotated[DepartmentNameSchema, Depends()]):
    return await DepartmentRepository.delete_department(department)
