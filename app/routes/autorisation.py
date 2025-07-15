from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, database

router = APIRouter(
    prefix="/autorisations",
    tags=["autorisations"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=schemas.AutorisationResponse,
    summary="Créer une nouvelle autorisation"
)
def create_autorisation(
    autorisation: schemas.AutorisationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_autorisation(db, autorisation)

@router.get(
    "/",
    response_model=List[schemas.AutorisationResponse],
    summary="Lister toutes les autorisations"
)
def list_autorisations(db: Session = Depends(get_db)):
    return crud.get_autorisations(db)

@router.get(
    "/etudiant/{etudiant_id}",
    response_model=List[schemas.AutorisationResponse],
    summary="Lister les autorisations d'un étudiant"
)
def get_autorisations_etudiant(
    etudiant_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_autorisations_by_etudiant(db, etudiant_id)

@router.delete(
    "/{autorisation_id}",
    summary="Supprimer une autorisation"
)
def delete_autorisation(
    autorisation_id: int,
    db: Session = Depends(get_db)
):
    autorisation = crud.delete_autorisation(db, autorisation_id)
    if not autorisation:
        raise HTTPException(status_code=404, detail="Autorisation non trouvée")
    return {"message": "Autorisation supprimée avec succès"}



from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/autorisations", tags=["autorisations"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/by-matricule/{matricule:path}",
    response_model=List[schemas.SalleResponse],
    summary="Liste des salles autorisées pour un matricule"
)
def get_salles_by_matricule(
    matricule: str,
    db: Session = Depends(get_db)
):
    etu = crud.get_etudiant_by_matricule(db, matricule)
    if not etu:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")

    autos = crud.get_autorisations_by_etudiant(db, etu.id)

    salles = []
    for a in autos:
        s = crud.get_salle_by_id(db, a.salle_id)
        if s:
            salles.append(s)
    return salles
