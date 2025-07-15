# Pour centraliser les imports si besoin
from .etudiant import router as etudiant_router
from .salle import router as salle_router
from .autorisation import router as autorisation_router
from .historique import router as historique_router
from app import database