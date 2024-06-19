from pydantic import BaseModel, ConfigDict


class SDepartment(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class SDepartmentName(BaseModel):
    name: str


class SDepartmentUpdate(BaseModel):
    name: str
    new_name: str


class SDepartmentUpdateResult(BaseModel):
    old_name: str
    new_name: str
    message: str = "Department {self.old_name} updated to {self.new_name}"
    status: str = "OK"


class SDepartmentDeleteResult(BaseModel):
    name: str
    message: str = "Department {self.name} deleted"
    status: str = 'OK'
