from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.company import Company
from app.services.audit import log_action
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/")
def list_companies(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    companies = db.query(Company).filter(
        Company.id == current_token["company_id"]
    ).all()

    return companies


@router.get("/{company_uuid}", response_model=CompanyResponse)
def get_company(
    company_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.uuid == company_uuid).first()

    if not company or company.id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company",
        )

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return company


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_company(
    data: CompanyCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    existing_company = db.query(Company).filter(
        Company.name == data.name
    ).first()

    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company name already exists",
        )

    company = Company(
        name=data.name,
        description=data.description,
        country=data.country,
        status="active",
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    log_action(
        db=db,
        user_id=current_token["user_id"],
        action="CREATE",
        entity_type="COMPANY",
        entity_id=company.id,
        details=f"Created company: {company.name}",
    )

    return company


@router.patch("/{company_uuid}", response_model=CompanyResponse)
def update_company(
    company_uuid: str,
    data: CompanyUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.uuid == company_uuid).first()

    if not company or company.id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company",
        )

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if data.name is not None:
        existing_company = db.query(Company).filter(
            Company.name == data.name,
            Company.id != company.id,
        ).first()

        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company name already exists",
            )

        company.name = data.name

    if data.description is not None:
        company.description = data.description

    if data.country is not None:
        company.country = data.country

    if data.status is not None:
        company.status = data.status

    db.commit()
    db.refresh(company)

    log_action(
        db=db,
        user_id=current_token["user_id"],
        action="UPDATE",
        entity_type="COMPANY",
        entity_id=company.id,
        details=f"Updated company: {company.name}",
    )

    return company
