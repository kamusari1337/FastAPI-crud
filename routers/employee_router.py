from fastapi import APIRouter

router = APIRouter(tags=["Employee API"], prefix="/employee")


@router.post("/")
async def add_employee():
    return


@router.get("/all/")
async def get_all_employees(id: int):
    return


@router.get("/")
async def get_one_employees():
    return


@router.patch("/")
async def update_employee():
    return


@router.delete("/")
async def delete_employee():
    return