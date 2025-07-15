from sqlalchemy import Column, String, TIMESTAMP, Integer, ForeignKey, CheckConstraint
from ..database import Base

class HistoriqueAcces(Base):
    __tablename__ = "historiques_acces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id", ondelete="SET NULL"))
    salle_id = Column(Integer, ForeignKey("salles.id", ondelete="SET NULL"))
    type_acces = Column(String(20), nullable=False)
    matricule_utilise = Column(String(50))
    date_entree = Column(TIMESTAMP, nullable=False)
    date_sortie = Column(TIMESTAMP)

    __table_args__ = (
        CheckConstraint("type_acces IN ('BLE', 'QR')", name="chk_type_acces_valide"),
    )
