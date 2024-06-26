from fastapi import HTTPException
from sqlalchemy import select, delete

from config.database import EmployeeOrm, SessionLocal, DepartmentOrm
from schemas.employee_schemas import EmployeeBaseSchema, EmployeeIdSchema, EmployeeUpdateSchema, \
    EmployeeUpdateResultSchema, EmployeeAddSchema, EmployeeDeleteResultSchema, EmployeeExceptionSchema


class EmployeeRepository:

    @classmethod
    async def add_employee(cls, employee: EmployeeAddSchema):
        async with SessionLocal() as session:
            try:
                department = await session.execute(
                    select(DepartmentOrm)
                    .where(DepartmentOrm.id == employee.department_id))
                if department.scalar_one_or_none() is None:
                    raise Exception("Department does not exist")
                employee = EmployeeOrm(**employee.model_dump())
                session.add(employee)

                await session.flush()
                await session.commit()

                return EmployeeBaseSchema.model_validate(employee)
            except Exception as e:
                await session.rollback()
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_employee(cls, employee: EmployeeIdSchema):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(EmployeeOrm)
                    .where(EmployeeOrm.id == employee.id))
                employee = result.scalar_one_or_none()
                if employee is None:
                    raise Exception("Employee does not exist")
                return EmployeeBaseSchema.model_validate(employee)
            except Exception as e:
                await session.rollback()
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_employees(cls):
        async with SessionLocal() as session:
            try:
                result = await session.execute(select(EmployeeOrm))
                employee_schema = [EmployeeBaseSchema.model_validate(employee_model)
                                   for employee_model in result.scalars()]

                if len(employee_schema) == 0:
                    return EmployeeExceptionSchema(message="No Employee exists")
                return employee_schema
            except Exception as e:
                await session.rollback()
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def update_employee(cls, employee: EmployeeUpdateSchema):
        async with SessionLocal() as session:
            try:
                result = await session.execute(
                    select(EmployeeOrm)
                    .where(EmployeeOrm.id == employee.id))
                old_employee = result.scalar_one_or_none()
                if old_employee is None:
                    raise Exception("Employee does not exist")

                old_employee.department_id = old_employee.id
                old_employee.name = employee.new_name
                old_employee.salary = employee.new_salary

                department_check = await session.execute(select(DepartmentOrm).where(DepartmentOrm.id == employee.department_id))
                if department_check.scalar_one_or_none() is None:
                    raise Exception("Department does not exist")

                await session.commit()

                return EmployeeUpdateResultSchema(old_department_id=old_employee.department_id,
                                                  old_name=old_employee.name,
                                                  old_salary=old_employee.salary,
                                                  new_department_id=employee.new_department_id,
                                                  new_name=employee.new_name,
                                                  new_salary=employee.new_salary)
            except Exception as e:
                await session.rollback()
                return HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def delete_employee(cls, employee: EmployeeIdSchema):
        async with SessionLocal() as session:
            try:
                check = await session.execute(
                    select(EmployeeOrm)
                    .where(EmployeeOrm.id == employee.id))
                if check.scalar_one_or_none() is None:
                    raise Exception("Employee does not exist")
                await session.execute(delete(EmployeeOrm).where(EmployeeOrm.id == employee.id))
                await session.commit()

                return EmployeeDeleteResultSchema(id=employee.id)
            except Exception as e:
                await session.rollback()
                return HTTPException(status_code=400, detail=str(e))
