from django.urls import path
from .views import AddDepenses
from .views import EntrepriseCreateView
<<<<<<< HEAD
from .views import AddRevenue, AddUtilisateur
from . import predictionDepense
from .generationRapport import generer_compteDeResultat,generer_bilan,generer_flux_de_tresorie
=======
from .views import AddRevenue 
from .views import DepensesListAPIView , RevenuesListView
>>>>>>> 8bfe9c25e17f84a5955e2122e28256257a19cc3a

urlpatterns = [
    path('add-depenses/', AddDepenses.as_view(), name='add-depenses'),
    path('add-entreprise/', EntrepriseCreateView.as_view(), name='add-entreprise'),
    path('add-revenue/', AddRevenue.as_view(), name='add-revenue'),
<<<<<<< HEAD
    path('add-utilisateur/', AddUtilisateur.as_view(), name='add-utilisateur'),
    path('prediction-depense/<int:user_id>/',predictionDepense.predict_expenses_view, name='predict_expenses'),
    path('generer-comptes-resultats/<int:user_id>/', generer_compteDeResultat, name='generer_compteDeResultat'),
    path('generer-bilan/<int:user_id>/', generer_bilan, name='generer_bilan'),
    path('generer-flux-tresorie/<int:user_id>/', generer_flux_de_tresorie, name='generer_flux_de_tresorie'),
=======
    path('depenses/', DepensesListAPIView.as_view(), name='depenses-list'),
    path('revenues/', RevenuesListView.as_view(), name='revenues-list'),

>>>>>>> 8bfe9c25e17f84a5955e2122e28256257a19cc3a
]
