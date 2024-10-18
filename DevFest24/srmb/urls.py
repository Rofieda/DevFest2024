from django.urls import path
from .views import AddDepenses
from .views import EntrepriseCreateView
from .views import AddRevenue 
from .views import DepensesListAPIView , RevenuesListView

urlpatterns = [
    path('add-depenses/', AddDepenses.as_view(), name='add-depenses'),
    path('add-entreprise/', EntrepriseCreateView.as_view(), name='add-entreprise'),
    path('add-revenue/', AddRevenue.as_view(), name='add-revenue'),
    path('depenses/', DepensesListAPIView.as_view(), name='depenses-list'),
    path('revenues/', RevenuesListView.as_view(), name='revenues-list'),

]
