from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from .base import Base

class Autorisation(Base):
    __tablename__ = "autorisations"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    etudiant_id  = Column(Integer, ForeignKey("etudiants.id",  ondelete="CASCADE"), nullable=False)
    salle_id     = Column(Integer, ForeignKey("salles.id",     ondelete="CASCADE"), nullable=False)
    niveau_acces = Column(String(50), default="standard")
    actif        = Column(Boolean, default=True)
    date_debut   = Column(TIMESTAMP, nullable=False)
    date_fin     = Column(TIMESTAMP, nullable=True)

    __table_args__ = (
        CheckConstraint("date_fin IS NULL OR date_fin > date_debut", name="chk_dates_valide"),
    )

    etudiant = relationship("Etudiant", back_populates="autorisations")
    salle    = relationship("Salle",    back_populates="autorisations")
