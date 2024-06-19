from pydantic import BaseModel, ConfigDict


class SEmployee(BaseModel):
    department_id: int
    name: str
    position: str = "manager" | "head"
    salary: int
    hire_date: str

    model_config = ConfigDict(from_attributes=True)
