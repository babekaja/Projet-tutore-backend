from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx

from .. import models, schemas, crud
from app import database

router = APIRouter(
    prefix="/etudiants",
    tags=["Etudiants"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create-from-matricule")
def create_etudiant_from_matricule(matricule: str, db: Session = Depends(get_db)):
    url = f"https://akhademie.ucbukavu.ac.cd/api/v1/school-students/read-by-matricule?matricule={matricule}"

    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Impossible de joindre le serveur Akhademie")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code,
                            detail="Erreur côté serveur Akhademie")

    data = response.json()

    if not data.get("data"):
        raise HTTPException(status_code=404, detail="Étudiant introuvable via le matricule")

    etudiant_data = data["data"]

    existing = db.query(models.Etudiant).filter(models.Etudiant.matricule == matricule).first()
    if existing:
        raise HTTPException(status_code=400, detail="Étudiant déjà enregistré localement.")

    # Nettoyage de l’email
    raw_email = etudiant_data.get("email") or f"{matricule.replace('/', '').replace('.', '')}@ucbukavu.ac.cd"
    email_sans_espace = raw_email.replace(" ", "")

    new_etudiant = models.Etudiant(
        matricule=etudiant_data["matricule"],
        nom=etudiant_data["name"],
        prenom=etudiant_data["firstname"],
        email=email_sans_espace,
        uid_firebase=f"AKH-{etudiant_data['id']}",
        date_creation=etudiant_data.get("createdAt")
    )

    db.add(new_etudiant)
    db.commit()
    db.refresh(new_etudiant)

    return {
        "message": "Étudiant ajouté avec succès",
        "etudiant": schemas.EtudiantResponse.model_validate(new_etudiant)
    }


@router.get("/", response_model=list[schemas.EtudiantResponse])
def list_etudiants(db: Session = Depends(get_db)):
    return crud.get_etudiants(db)

@router.get("/{etudiant_id}", response_model=schemas.EtudiantResponse)
def get_etudiant(etudiant_id: str, db: Session = Depends(get_db)):
    etudiant = crud.get_etudiant_by_id(db, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return etudiant

@router.delete("/{etudiant_id}")
def delete_etudiant(etudiant_id: str, db: Session = Depends(get_db)):
    etudiant = crud.delete_etudiant(db, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return {"message": "Étudiant supprimé avec succès"}
