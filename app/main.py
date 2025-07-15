from fastapi import FastAPI

from app.routes import etudiant, autorisation
from app.routes import historique, salle

app = FastAPI(
    title="Access Control API",
    version="1.0.0"
)

app.include_router(etudiant.router)
app.include_router(salle.router)
app.include_router(autorisation.router)
app.include_router(historique.router)


