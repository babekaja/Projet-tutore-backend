from sqlalchemy.orm import Session
from .. import models, schemas

def create_autorisation(db: Session, autorisation: schemas.AutorisationCreate):
    db_autorisation = models.Autorisation(**autorisation.dict())
    db.add(db_autorisation)
    db.commit()
    db.refresh(db_autorisation)
    return db_autorisation

def get_autorisations(db: Session):
    return db.query(models.Autorisation).all()

def get_autorisations_by_etudiant(db: Session, etudiant_id):
    return db.query(models.Autorisation).filter(models.Autorisation.etudiant_id == etudiant_id).all()

def delete_autorisation(db: Session, autorisation_id):
    autorisation = db.query(models.Autorisation).filter(models.Autorisation.id == autorisation_id).first()
    if autorisation:
        db.delete(autorisation)
        db.commit()
    return autorisation
