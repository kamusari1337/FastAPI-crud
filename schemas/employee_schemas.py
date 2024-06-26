from pydantic import Field, validator

from schemas import BaseSchema


class EmployeeBaseSchema(BaseSchema):
    id: int = Field(gt=0, description='Department ID')
    department_id: int = Field(gt=0, description='Department ID')
    name: str
    salary: int = Field(gt=0, lt=500_000, description='Department ID')


class EmployeeAddSchema(BaseSchema):
    department_id: int = Field(gt=0, description='Department ID')
    name: str
    salary: int = Field(gt=0, lt=500_000, description='Department ID')


class EmployeeIdSchema(BaseSchema):
    id: int = Field(gt=0, description='Department ID')


class EmployeeUpdateSchema(BaseSchema):
    id: int = Field(gt=0, description='Department ID')
    new_department_id: int = Field(gt=0, description='Department ID')
    new_name: str
    new_salary: int = Field(gt=0, lt=500_000, description='Department ID')


class EmployeeUpdateResultSchema(BaseSchema):
    old_department_id: int = Field(gt=0, description='Department ID')
    old_name: str
    old_salary: int = Field(gt=0, lt=500_000, description='Department ID')
    new_department_id: int = Field(gt=0, description='Department ID')
    new_name: str
    new_salary: int = Field(gt=0, lt=500_000, description='Department ID')
    message: str = "Employee name updated"


class EmployeeDeleteResultSchema(BaseSchema):
    id: int = Field(gt=0, description='Department ID')
    message: str = "Employee deleted"


class EmployeeExceptionSchema(BaseSchema):
    message: str
