from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from config.database import DepartmentOrm, SessionLocal
from config.logger import logger
from schemas.department_schemas import (DepartmentBaseSchema, DepartmentDeleteResultSchema,
                                        DepartmentNameSchema, DepartmentUpdateSchema,
                                        DepartmentUpdateResultSchema, DepartmentExceptionSchema)


class DepartmentRepository:

    @classmethod
    async def add_department(cls, department: DepartmentNameSchema):
        async with SessionLocal() as session:
            try:
                department = DepartmentOrm(**department.model_dump())
                session.add(department)
                await session.flush()
                await session.commit()
                logger.info(f"Added department with id {department.id} and name {department.name}")
                return DepartmentBaseSchema.model_validate(department)
            except IntegrityError as e:
                await session.rollback()
                logger.error(e)
                raise HTTPException(status_code=400, detail="Department with the given name already exists")
            except Exception as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_department(cls, department: DepartmentNameSchema):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(DepartmentOrm)
                    .where(DepartmentOrm.name == department.name))
                department = result.scalar_one_or_none()
                if department is None:
                    raise Exception("Department does not exist")
                logger.info(f"Selected department with name {department.name}")
                return DepartmentBaseSchema.model_validate(department)
            except IntegrityError as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail="Department with the given name already exists")
            except Exception as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_departments(cls):
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(DepartmentOrm))
                department_schemas = [DepartmentBaseSchema.model_validate(department_model)
                                      for department_model in result.scalars()]
                if len(department_schemas) == 0:
                    return DepartmentExceptionSchema(message="No Departments exists")
                logger.info(f"Selected all department")
                return department_schemas
            except Exception as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def update_department(cls, department: DepartmentUpdateSchema):
        async with SessionLocal() as session:
            try:
                await session.execute(update(DepartmentOrm)
                                      .where(DepartmentOrm.name == department.name)
                                      .values(name=department.new_name))
                await session.commit()
                logger.info(f"Updating department with name: {department.name} to {department.new_name}")
                return DepartmentUpdateResultSchema(old_name=department.name, new_name=department.new_name)
            except IntegrityError as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail="Department with the given name already exists")
            except Exception as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def delete_department(cls, department: DepartmentNameSchema):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(DepartmentOrm)
                    .where(DepartmentOrm.name == department.name)
                )
                department = result.scalar_one_or_none()
                if department is None:
                    raise Exception("Department does not exist")
                await session.delete(department)
                await session.commit()
                logger.info(f"Deleted department with name: {department.name}")
                return DepartmentDeleteResultSchema(name=department.name)
            except Exception as e:
                await session.rollback()
                logger.error(e)
                return HTTPException(status_code=400, detail=str(e))
