from sqlalchemy import delete, select, update

from config.database import DepartmentOrm, SessionLocal
from schemas.department_schemas import (SDepartment, SDepartmentDeleteResult,
                                        SDepartmentName, SDepartmentUpdate,
                                        SDepartmentUpdateResult)


class DepartmentRepository:

    @classmethod
    async def add_department(cls, department: SDepartmentName) -> SDepartment:
        async with SessionLocal() as session:
            department_dict = department.model_dump()

            department = DepartmentOrm(**department_dict)

            session.add(department)
            await session.flush()
            await session.commit()

            return SDepartment.model_validate(department)

    @classmethod
    async def get_department(cls, department: SDepartmentName) -> SDepartment:
        async with SessionLocal() as session:
            query = select(DepartmentOrm).where(DepartmentOrm.name == department.name)

            department_model = await session.scalar(query)

            return SDepartment.model_validate(department_model)

    @classmethod
    async def get_departments(cls) -> list[SDepartment]:
        async with SessionLocal() as session:
            query = select(DepartmentOrm)
            department_models = await session.scalars(query)

            department_schemas = [SDepartment.model_validate(department_model) for department_model in
                                  department_models]

            return department_schemas

    @classmethod
    async def update_department(cls, department: SDepartmentUpdate) -> SDepartmentUpdateResult:
        async with SessionLocal() as session:
            update(DepartmentOrm).where(DepartmentOrm.name == department.name).values(name=department.new_name)

            await session.commit()

            return SDepartmentUpdateResult(old_name=department.name, new_name=department.new_name)

    @classmethod
    async def delete(cls, department: SDepartmentName) -> SDepartmentDeleteResult:
        async with SessionLocal() as session:
            delete(DepartmentOrm).where(DepartmentOrm.name == department.name)

            await session.commit()

            return SDepartmentDeleteResult(name=department.name)
