from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Mapped, backref,
                            mapped_column, relationship)

DATABASE_URL = "sqlite+aiosqlite:///HR_department.db"
DATABASE_ENGINE = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=DATABASE_ENGINE, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class DepartmentOrm(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    employees = relationship("EmployeeOrm", back_populates="department",
                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return (f"ID: {self.id}, "
                f"Name: {self.name}")


class EmployeeOrm(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)

    department = relationship("DepartmentOrm", back_populates="employees")

    def __repr__(self):
        return (f"ID: {self.id}, "
                f"Department ID: {self.department_id}, "
                f"Name: {self.name}, "
                f"Salary: {self.salary}")


async def create_tables():
    async with DATABASE_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with DATABASE_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
