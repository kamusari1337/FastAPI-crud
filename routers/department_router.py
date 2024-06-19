from typing import Annotated

from fastapi import APIRouter, Depends
from repositories.department_repository import DepartmentRepository
from schemas.department_schemas import (SDepartment, SDepartmentDeleteResult,
                                        SDepartmentName, SDepartmentUpdate,
                                        SDepartmentUpdateResult)

router = APIRouter(tags=["Department API"], prefix="/department")


@router.post("/add_one/")
async def add_department(
    department: Annotated[SDepartmentName, Depends()]
    ) -> SDepartment:
    
    return await DepartmentRepository.add_department(department)


@router.get("/get_one/")
async def get_one_departments(
    department: Annotated[SDepartmentName, Depends()]
    ) -> SDepartment:
    
    return await DepartmentRepository.get_department(department)


@router.get("/all/")
async def get_all_departments() -> list[SDepartment]:
    
    return await DepartmentRepository.get_departments()


@router.patch("/update_one/")
async def update_department(
    department: Annotated[SDepartmentUpdate, Depends()]
    ) -> SDepartmentUpdateResult:
    
    return await DepartmentRepository.update_department(department)


@router.delete("/delete/")
async def delete_department(
    department: Annotated[SDepartmentName, Depends()]
    ) -> SDepartmentDeleteResult:
    
    return await DepartmentRepository.delete_department(department)
