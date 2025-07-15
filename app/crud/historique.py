from sqlalchemy.orm import Session
from .. import models, schemas

def create_historique(db: Session, historique: schemas.HistoriqueCreate):
    db_historique = models.HistoriqueAcces(**historique.dict())
    db.add(db_historique)
    db.commit()
    db.refresh(db_historique)
    return db_historique

def get_historiques(db: Session):
    return db.query(models.HistoriqueAcces).all()

def get_historiques_by_etudiant(db: Session, etudiant_id):
    return db.query(models.HistoriqueAcces).filter(models.HistoriqueAcces.etudiant_id == etudiant_id).all()

def get_historiques_by_salle(db: Session, salle_id):
    return db.query(models.HistoriqueAcces).filter(models.HistoriqueAcces.salle_id == salle_id).all()
