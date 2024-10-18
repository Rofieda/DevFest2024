from django.urls import path
from .views import AddDepenses
from .views import EntrepriseCreateView
from .views import AddRevenue

urlpatterns = [
    path('add-depenses/', AddDepenses.as_view(), name='add-depenses'),
    path('add-entreprise/', EntrepriseCreateView.as_view(), name='add-entreprise'),
    path('add-revenue/', AddRevenue.as_view(), name='add-revenue'),

]
