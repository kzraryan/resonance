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
    department = Column(String, nullable=False)  # CS/MATH
    position = Column(String, nullable=False)  # Student/Professor

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

    research_domain = Column(String)  # e.g., "Oncology", "Neuroscience"
    llm_usage = Column(String)  # e.g., "GPT-4"
    which_deep_learning_usage = Column(String)  # e.g., "CNN", "Transformer"
    which_machine_learning = Column(String)  # e.g., "SVM", "RandomForest"
    datasets = Column(String)  # e.g., "TCGA", "ImageNet"
    data_category = Column(String)  # e.g., "Genomics", "Radiology"
    dataset_size = Column(String)  # e.g., "Large", "Small"
    data_type = Column(String)  # e.g., "Tabular", "Imaging"
    specific_algorithms = Column(String)  # e.g., "ResNet", "K-means"
    programming_languages = Column(String)  # e.g., "Python", "R"
    programming_libraries = Column(String)  # e.g., "TensorFlow", "scikit-learn"
    funding = Column(String)  # e.g., "NIH", "No funding"
    timeline = Column(String)  # e.g., "Long-term", "Short-term"
    problem_type = Column(String)  # e.g., "Classification", "Regression"
    ethical_considerations = Column(String)  # e.g., "IRB"
    type_of_study = Column(String)  # e.g., "Prospective", "Retrospective"
    code_and_reproducibility = Column(String)  # e.g., "Open-source", "Not reproducible"
    benchmarking = Column(String)  # e.g., "State-of-art", "Baseline"

    # Back-populate with Publication model.
    publication = relationship("Publication", back_populates="publication_metadata")


class Search(Base):
    __tablename__ = "searches"

    # Primary key for each search query
    id = Column(Integer, primary_key=True, autoincrement=True)  # Search_ID
    researcher_id = Column(Integer, ForeignKey("researchers.id"), nullable=False)
    search_text = Column(Text, nullable=False)

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
