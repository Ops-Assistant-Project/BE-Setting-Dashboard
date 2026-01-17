from models.employee import Employee
from services.crud_base import CrudBase


class EmployeeService(CrudBase):
    model = Employee