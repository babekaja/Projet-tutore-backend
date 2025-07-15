from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import models, schemas
from fastapi import HTTPException


def create_etudiant(db: Session, etudiant: schemas.EtudiantCreate) -> models.Etudiant:
    db_etudiant = models.Etudiant(**etudiant.dict())
    db.add(db_etudiant)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement : {str(e)}")

    # Vérifie si l'ID est bien généré
    if not db_etudiant.id:
        raise HTTPException(status_code=500, detail="Impossible de récupérer l'ID de l'étudiant après insertion")

    db.refresh(db_etudiant)
    return db_etudiant


def get_etudiant_by_id(db: Session, etudiant_id: int) -> models.Etudiant | None:
    return db.query(models.Etudiant).filter(models.Etudiant.id == etudiant_id).first()


def get_etudiant_by_matricule(db: Session, matricule: str) -> models.Etudiant | None:
    return db.query(models.Etudiant).filter(models.Etudiant.matricule == matricule).first()


def get_etudiants(db: Session) -> list[models.Etudiant]:
    return db.query(models.Etudiant).all()


def delete_etudiant(db: Session, etudiant_id: int) -> models.Etudiant | None:
    etudiant = get_etudiant_by_id(db, etudiant_id)
    if etudiant:
        try:
            db.delete(etudiant)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression : {str(e)}")
    return etudiant
