from models.models import Researcher


def create_researcher(db, orcid_id: str, full_name: str, department:str, position:str) -> Researcher:
    # Create a new Researcher record using the provided ORCID ID and full name.
    new_researcher = Researcher(orcid_id=orcid_id, full_name=full_name, department=department, position=position)
    db.add(new_researcher)
    db.commit()
    db.refresh(new_researcher)
    return new_researcher

def get_researcher_by_orcid(db, orcid_id: str) -> Researcher:
    # Retrieve a Researcher by their ORCID ID.
    return db.query(Researcher).filter(Researcher.orcid_id == orcid_id).first()

def get_researcher_by_id(db, id: int) -> Researcher:
    return db.query(Researcher).filter(Researcher.id == id).first()

def get_researcher_by_name(db, full_name: str) -> Researcher:
    return db.query(Researcher).filter(Researcher.full_name == full_name).first()

def get_all_researchers(db):
    # Return all Researcher records.
    return db.query(Researcher).all()
