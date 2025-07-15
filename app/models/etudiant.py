from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base

class Etudiant(Base):
    __tablename__ = "etudiants"

    id            = Column(Integer, primary_key=True, autoincrement=True, index=True)
    matricule     = Column(String(50), unique=True, nullable=False)
    nom           = Column(String(100), nullable=False)
    prenom        = Column(String(100), nullable=True)
    email         = Column(String(150), unique=True, nullable=False)
    uid_firebase  = Column(String(128), unique=True, nullable=False)
    date_creation = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relation inverse vers Autorisation
    autorisations = relationship(
        "Autorisation",
        back_populates="etudiant",
        cascade="all, delete-orphan",
    )


