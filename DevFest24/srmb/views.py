from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Depenses ,Entreprise , Revenue
from .serializers import DepensesSerializer ,RevenueSerializer
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
    

class DepensesListAPIView(generics.ListAPIView):
    queryset = Depenses.objects.all()
    serializer_class = DepensesSerializer


class RevenuesListView(APIView):
    def get(self, request):
        revenues = Revenue.objects.all()
        serializer = RevenueSerializer(revenues, many=True)
        return Response(serializer.data)