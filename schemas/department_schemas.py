from schemas import BaseSchema


class DepartmentBaseSchema(BaseSchema):
    id: int
    name: str


class DepartmentNameSchema(BaseSchema):
    name: str


class DepartmentUpdateSchema(BaseSchema):
    name: str
    new_name: str


class DepartmentUpdateResultSchema(BaseSchema):
    old_name: str
    new_name: str
    message: str = "Department name updated"


class DepartmentDeleteResultSchema(BaseSchema):
    name: str
    message: str = "Department deleted"


class DepartmentExceptionSchema(BaseSchema):
    message: str
