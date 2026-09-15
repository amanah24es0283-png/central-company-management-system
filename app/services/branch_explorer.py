from sqlalchemy.orm import Session

from app.models.branch import Branch


def search_branches(
    db: Session,
    company_id: int,
    search: str | None = None,
    country: str | None = None,
    city: str | None = None,
    status: str | None = None,
):
    query = (
        db.query(Branch)
        .filter(Branch.company_id == company_id)
    )

    if search:
        search_value = f"%{search}%"

        query = query.filter(
            Branch.name.ilike(search_value)
            | Branch.city.ilike(search_value)
            | Branch.address.ilike(search_value)
        )

    if country:
        query = query.filter(Branch.country == country)

    if city:
        query = query.filter(Branch.city == city)

    if status:
        query = query.filter(Branch.status == status)

    return query.order_by(Branch.id).all()
