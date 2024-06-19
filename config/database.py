from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, backref, declarative_base,
                            mapped_column, relationship)

DATABASE_URL = "sqlite+aiosqlite:///HR_department.db"
DATABASE_ENGINE = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=DATABASE_ENGINE, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DepartmentOrm(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    amount: Mapped[int]

    employees = relationship("EmployeeOrm", backref="department")

    def __repr__(self):
        return f"Department: [ID: {self.id}, Name: {self.name}]"


class EmployeeOrm(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    name: Mapped[str]
    position: Mapped[str]
    salary: Mapped[int]
    hire_date: Mapped[str]

    department = relationship("DepartmentOrm", backref=backref('employees'))

    def __repr__(self):
        return f"Employee: [ID: {self.id}, Department ID: {self.department_id}, Name: {self.name}, Position: {self.position}, Salary: {self.salary}, Hire Date: {self.hire_date}]"


async def create_tables():
    async with DATABASE_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with DATABASE_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
