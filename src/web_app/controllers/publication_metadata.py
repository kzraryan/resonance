from models.models import PublicationMetadata



def create_publication_metadata(db, publication_id: int, metadata: dict) -> PublicationMetadata:
    # Create a new metadata record for a Publication.
    new_metadata = PublicationMetadata(publication_id=publication_id, **metadata)
    db.add(new_metadata)
    db.commit()
    db.refresh(new_metadata)
    return new_metadata

def get_metadata_by_publication(db, publication_id: int) -> PublicationMetadata:
    # Retrieve metadata for a specific Publication.
    return db.query(PublicationMetadata).filter(PublicationMetadata.publication_id == publication_id).first()





