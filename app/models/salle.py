from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base

class Salle(Base):
    __tablename__ = "salles"

    id            = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nom_salle     = Column(String(100), nullable=False)
    localisation  = Column(String(255), nullable=True)
    description   = Column(String(255), nullable=True)
   # date_creation = Column(TIMESTAMP, nullable=False, server_default=func.now())

    # Relation inverse vers Autorisation
    autorisations = relationship(
        "Autorisation",
        back_populates="salle",
        cascade="all, delete-orphan",
    )
