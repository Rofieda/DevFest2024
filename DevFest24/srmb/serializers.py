from rest_framework import serializers
from .models import Depenses , Entreprise ,Revenue

class DepensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depenses
        fields = '__all__'  # This will include all fields from the Depenses model


class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = '__all__'  # You can specify fields explicitly if needed


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'entreprise', 'montant', 'date', 'categorie', 'description']  # Specify the fields to be serialized

    def create(self, validated_data):
        # This method can be overridden if you need custom logic when creating a Revenue instance
        return super().create(validated_data)
    


# myapp/serializers.py

from .models import Utilisateur, Entreprise

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'password', 'entreprise']

    def create(self, validated_data):
        user = Utilisateur(**validated_data)
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

