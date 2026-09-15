from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch


def get_employee_report(
    db: Session,
    company_id: int,
):
    employees = (
        db.query(
            Employee,
            Department.name.label("department_name"),
            Department.branch_id.label("branch_id"),
            Branch.name.label("branch_name"),
        )
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .order_by(Employee.id)
        .all()
    )

    return {
        "company_id": company_id,
        "count": len(employees),
        "employees": [
            {
                "employee_id": employee.id,
                "employee_code": employee.employee_code,
                "job_title": employee.job_title,
                "status": employee.status,
                "department_id": employee.department_id,
                "department_name": department_name,
                "branch_id": branch_id,
                "branch_name": branch_name,
            }
            for employee, department_name, branch_id, branch_name in employees
        ],
    }
