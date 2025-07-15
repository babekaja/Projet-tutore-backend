from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def create_salle(db: Session, salle: schemas.SalleCreate):
    db_salle = models.Salle(
        nom_salle=salle.nom_salle,
        localisation=salle.localisation,
        description=salle.description,

    )
    db.add(db_salle)
    db.commit()
    db.refresh(db_salle)
    return db_salle

def get_salle_by_id(db: Session, salle_id: int):
    return db.query(models.Salle).filter(models.Salle.id == salle_id).first()

def get_salles(db: Session):
    return db.query(models.Salle).all()

def delete_salle(db: Session, salle_id: int):
    salle = get_salle_by_id(db, salle_id)
    if salle:
        db.delete(salle)
        db.commit()
    return salle
