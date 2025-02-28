from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def to_dict(model_instance):
    # Convert a SQLAlchemy model instance to a dictionary.
    return {col.name: getattr(model_instance, col.name) for col in model_instance.__table__.columns}


class Researcher(Base):
    __tablename__ = "researchers"

    # Primary key for each researcher
    id = Column(Integer, primary_key=True, autoincrement=True)  # Researcher_ID
    orcid_id = Column(String, unique=True)  # ORCID_ID
    full_name = Column(String, nullable=False)  # Full Name

    # One-to-many relationships: a researcher can have many publications and searches
    publications = relationship("Publication", back_populates="researcher")
    searches = relationship("Search", back_populates="researcher")


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    researcher_id = Column(Integer, ForeignKey("researchers.id"), nullable=False)
    doi = Column(String, nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(Text)
    year = Column(Integer)

    researcher = relationship("Researcher", back_populates="publications")
    publication_metadata = relationship("PublicationMetadata", back_populates="publication", uselist=False)

    __table_args__ = (
        UniqueConstraint("researcher_id", "doi", name="uix_researcher_doi"),
    )


class PublicationMetadata(Base):
    __tablename__ = "publication_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), unique=True, nullable=False)

    research_category = Column(String)
    which_llm_used = Column(String)
    what_datasets = Column(String)
    type_of_data = Column(String)
    machine_learning_deep_learning = Column(String)
    specific_algorithms = Column(String)
    which_languages = Column(String)
    which_libraries = Column(String)
    funding_for_research = Column(String)
    cross_disciplinary_stuff = Column(String)
    timeline = Column(String)
    dataset_size = Column(String)
    problem_type = Column(String)
    data_type = Column(String)
    ethical_considerations = Column(String)
    summary_of_innovation = Column(String)
    type_of_study = Column(String)
    code_and_reproducibility = Column(String)
    important_citations = Column(String)
    benchmarking = Column(String)

    # Back-populate using the updated attribute name in Publication.
    publication = relationship("Publication", back_populates="publication_metadata")


class Search(Base):
    __tablename__ = "searches"

    # Primary key for each search query
    id = Column(Integer, primary_key=True, autoincrement=True)  # Search_ID
    researcher_id = Column(Integer, ForeignKey("researchers.id"), nullable=False)
    query = Column(Text, nullable=False)

    # Relationship: a search belongs to a researcher and has many results
    researcher = relationship("Researcher", back_populates="searches")
    results = relationship("SearchResult", back_populates="search", cascade="all, delete-orphan")


class SearchResult(Base):
    __tablename__ = "search_results"

    # Composite primary key: links a search to a publication (research article)
    search_id = Column(Integer, ForeignKey("searches.id"), primary_key=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), primary_key=True)
    order_index = Column(Integer, nullable=False)

    # Relationships linking back to search and publication
    search = relationship("Search", back_populates="results")
    publication = relationship("Publication")
