from fastapi import APIRouter, HTTPException
from services.employee import EmployeeService
from schemas.employee import EmployeeCreateSchema, EmployeeUpdateSchema


router = APIRouter(prefix="/employee", tags=["Employees"])


@router.post("/", summary="Create employee")
def create_employee(payload: EmployeeCreateSchema):
    try:
        employee_id = EmployeeService.create(payload.dict())
        return {"id": employee_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}", summary="Get employee by id")
def get_employee(employee_id: str):
    employee = EmployeeService.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.get("/", summary="List employees")
def list_employees():
    return EmployeeService.list()


@router.patch("/{employee_id}", summary="Update employees")
def update_employees(employee_id: str, payload: EmployeeUpdateSchema):
    success = EmployeeService.update(employee_id, payload.model_dump(exclude_unset=True))

    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "updated"}


@router.delete("/{employee_id}", summary="Delete employee")
def delete_employee(employee_id: str):
    success = EmployeeService.delete(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "deleted"}