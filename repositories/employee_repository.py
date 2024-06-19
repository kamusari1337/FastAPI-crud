from config.database import EmployeeOrm, SessionLocal
from schemas.employee_schemas import SEmployee


class EmployeeRepository:

	@classmethod
	async def add(cls, employee: SEmployee) -> SEmployee:
		async with SessionLocal() as session:
			employee_dict = employee.model_dump()

			employee = EmployeeOrm(**employee_dict)

			session.add(employee)
			await session.flush()
			await session.commit()

			return SEmployee.model_validate(employee)
