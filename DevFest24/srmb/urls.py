from django.urls import path
from .views import AddDepenses
from .views import EntrepriseCreateView
from .views import AddRevenue
from .views import SignUpView, LoginView, LogoutView


urlpatterns = [
    path('add-depenses/', AddDepenses.as_view(), name='add-depenses'),
    path('add-entreprise/', EntrepriseCreateView.as_view(), name='add-entreprise'),
    path('add-revenue/', AddRevenue.as_view(), name='add-revenue'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]


