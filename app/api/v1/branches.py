from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate, BranchResponse

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/")
def list_branches(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    branches = db.query(Branch).filter(
        Branch.company_id == current_token["company_id"]
    ).all()

    return branches


@router.get("/{branch_uuid}", response_model=BranchResponse)
def get_branch(
    branch_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    branch = db.query(Branch).filter(
        Branch.uuid == branch_uuid
    ).first()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )

    if branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this branch",
        )

    return branch


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_branch(
    data: BranchCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    if data.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a branch for another company",
        )

    branch = Branch(
        company_id=data.company_id,
        name=data.name,
        country=data.country,
        city=data.city,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        status="active",
    )

    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch


@router.patch("/{branch_uuid}", response_model=BranchResponse)
def update_branch(
    branch_uuid: str,
    data: BranchUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    branch = db.query(Branch).filter(
        Branch.uuid == branch_uuid
    ).first()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )

    if branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this branch",
        )

    if data.name is not None:
        branch.name = data.name

    if data.country is not None:
        branch.country = data.country

    if data.city is not None:
        branch.city = data.city

    if data.address is not None:
        branch.address = data.address

    if data.latitude is not None:
        branch.latitude = data.latitude

    if data.longitude is not None:
        branch.longitude = data.longitude

    if data.status is not None:
        branch.status = data.status

    db.commit()
    db.refresh(branch)

    return branch
