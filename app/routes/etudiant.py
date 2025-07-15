from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import httpx
from .. import models, schemas


from app import database
from .. import crud, schemas

router = APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()




router = APIRouter(
    prefix="/etudiants",
    tags=["Etudiants"]
)


@router.post("/create-from-matricule")
def create_etudiant_from_matricule(matricule: str, db: Session = Depends(get_db)):
    url = f"https://akhademie.ucbukavu.ac.cd/api/v1/school-students/read-by-matricule?matricule={matricule}"

    # Appel API externe
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="Impossible de joindre le serveur Akhademie")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Erreur côté serveur Akhademie")

    data = response.json()

    if not data.get("data"):
        raise HTTPException(status_code=404, detail="Étudiant introuvable via le matricule")

    etudiant_data = data["data"]

    # Vérifie si l’étudiant existe déjà dans ta base
    existing = db.query(models.Etudiant).filter(models.Etudiant.matricule == matricule).first()
    if existing:
        raise HTTPException(status_code=400, detail="Étudiant déjà enregistré localement.")

    # Créer un nouvel étudiant localement
    new_etudiant = models.Etudiant(
        matricule=etudiant_data["matricule"],
        nom=etudiant_data["name"],  # ou etudiant_data["lastname"] selon ton besoin
        prenom=etudiant_data["firstname"],
        email=etudiant_data.get("email") or f"{matricule.replace('/', '').replace('.', '')}@ucbukavu.ac.cd",
        uid_firebase=f"AKH-{etudiant_data['id']}",  # ou un autre système si nécessaire
        date_creation=etudiant_data.get("createdAt")
    )

    db.add(new_etudiant)
    db.commit()
    db.refresh(new_etudiant)

    return {
        "message": "Étudiant ajouté avec succès",
        "etudiant": {
            "id": new_etudiant.id,
            "matricule": new_etudiant.matricule,
            "nom": new_etudiant.nom,
            "prenom": new_etudiant.prenom,
            "email": new_etudiant.email
        }
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
