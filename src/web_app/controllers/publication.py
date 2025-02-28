from controllers.researcher import get_researcher_by_id
from models.models import Publication
from utils.importing_publications import get_publication_data

def create_publication(db, researcher_id: int, title: str, abstract: str, year: int, doi: str) -> Publication:
    """
    Create a new Publication record with DOI.
    """
    new_publication = Publication(
        researcher_id=researcher_id,
        title=title,
        abstract=abstract,
        year=year,
        doi=doi
    )
    db.add(new_publication)
    db.commit()
    db.refresh(new_publication)
    return new_publication

def get_publication_by_id(db, publication_id: int) -> Publication:
    # Retrieve a Publication by its ID.
    return db.query(Publication).filter(Publication.id == publication_id).first()

def get_publication_by_doi(db, researcher_id: int, doi: str) -> Publication:
    """
    Retrieve a Publication record by researcher and DOI.
    """
    return db.query(Publication).filter(
        Publication.researcher_id == researcher_id,
        Publication.doi == doi
    ).first()

def get_publications_by_researcher(db, researcher_id: int):
    # Get all Publications associated with a given Researcher.
    return db.query(Publication).filter(Publication.researcher_id == researcher_id).all()


def import_publications_from_online(db, researcher_id: int) -> list[Publication]:
    # Retrieve the researcher record using the provided researcher_id.
    researcher = get_researcher_by_id(db, researcher_id)
    if not researcher:
        return []

    # Extract the ORCID ID from the researcher record.
    orcid_id = researcher.orcid_id

    # Fetch publication data using the ORCID ID.
    publications_data = get_publication_data([{"orcid_id": orcid_id}])

    imported_publications = []
    for pub_data in publications_data:
        # Create a Publication instance without adding it to the DB.
        # These are transient objects that the user can later choose to submit.
        publication = Publication(
            researcher_id=researcher_id,
            title=pub_data["title"],
            abstract=pub_data["abstract"],
            year=pub_data["year"],
            doi=pub_data["doi"]
        )
        imported_publications.append(publication)

    return imported_publications


def include_publications(db, researcher_id: int, publications_data: list) -> list[Publication]:
    """
    For each publication in the provided data list, check if a publication with the same DOI
    already exists for this researcher. If not, create a new Publication record.

    publications_data: List of dicts with keys "doi", "title", "abstract", "year"
    """
    included_publications = []
    for pub_data in publications_data:
        doi = pub_data.get("doi")
        # Check if the publication already exists for the researcher using the DOI.
        existing_pub = get_publication_by_doi(db, researcher_id, doi)
        if existing_pub:
            continue  # Skip duplicate entry

        # Create a new publication with DOI.
        new_pub = create_publication(
            db,
            researcher_id,
            title=pub_data["title"],
            abstract=pub_data["abstract"],
            year=pub_data["year"],
            doi=doi
        )
        included_publications.append(new_pub)

    return included_publications

