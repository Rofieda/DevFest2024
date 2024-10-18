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
    
class DepensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depenses
        fields = '__all__'  # Or specify the fields you want to expose


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'entreprise', 'montant', 'date', 'categorie', 'description', 'type_flux_tresorerie']  # Add the field here