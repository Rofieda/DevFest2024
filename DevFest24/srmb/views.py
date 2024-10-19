from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Depenses ,Entreprise, Revenue
from .serializers import DepensesSerializer ,RevenueSerializer, UtilisateurSerializer
from rest_framework import generics
from .serializers import EntrepriseSerializer

class EntrepriseCreateView(APIView):
    def post(self, request):
        serializer = EntrepriseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the valid data into the Entreprise model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddDepenses(APIView):
    def post(self, request):
        serializer = DepensesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the valid data into the Depenses model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddRevenue(APIView):
    def post(self, request):
        serializer = RevenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the valid data into the Revenue model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

 # myapp/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from .models import Utilisateur, Entreprise
from .serializers import UserSerializer, LoginSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        entreprise = Entreprise.objects.get(id=user.entreprise.id)
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return Response({
                'user': UserSerializer(user).data, 
                'entreprise': {
                    'name': entreprise.name,
                    'email': entreprise.email,
                    'address': entreprise.address,
                    'phone': entreprise.phone
                },
                'entreprise': {
                    'name': entreprise.name,
                    'email': entreprise.email,
                    'address': entreprise.address,
                    'phone': entreprise.phone
                },
                'detail': 'Login successful.'
            }, status=status.HTTP_200_OK)
        else:
            # Return an error message for invalid credentials
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import IntegrityError

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        entreprise_name = request.data.get('entreprise_name')
        entreprise_email = request.data.get('entreprise_email')
        entreprise_address = request.data.get('entreprise_address')
        entreprise_phone = request.data.get('entreprise_phone')

        # Check if the username already exists
        if Utilisateur.objects.filter(username=username).exists():
            return Response(
                {'error': 'User with this username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get or create the Entreprise
        entreprise, created = Entreprise.objects.get_or_create(
            email=entreprise_email,
            defaults={
                'name': entreprise_name,
                'address': entreprise_address,
                'phone': entreprise_phone,
            }
        )

        try:
            # Create the user
            user = Utilisateur.objects.create_user(username=username, password=password, entreprise=entreprise)
        except IntegrityError:
            return Response(
                {'error': 'An error occurred while creating the user.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Return success response
        return Response(
            {
                'user': UserSerializer(user).data, 
                'entreprise': {
                    'name': entreprise.name,
                    'email': entreprise.email,
                    'address': entreprise.address,
                    'phone': entreprise.phone
                }
            },
            status=status.HTTP_201_CREATED
        )

    
class DepensesListAPIView(generics.ListAPIView):
     queryset = Depenses.objects.all()
     serializer_class = DepensesSerializer

class RevenuesListView(APIView):
    def get(self, request):
        revenues = Revenue.objects.all()
        serializer = RevenueSerializer(revenues, many=True)
        return Response(serializer.data)
    
class AddUtilisateur(APIView):
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the valid data into the Utilisateur model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
