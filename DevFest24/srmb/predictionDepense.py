from django.shortcuts import render
from django.http import JsonResponse
import os
import django
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from .models import Depenses, Utilisateur

# Récupérer les données de la base de données
def get_expenses_data(entreprise_id):
    expenses = Depenses.objects.filter(entreprise=entreprise_id).order_by('date')
    
    X = []  # Contiendra les indices temporels
    y = []  # Contiendra les montants des dépenses
    
    for i, depense in enumerate(expenses):
        X.append([i]) 
        y.append(float(depense.montant))
    
    return np.array(X), np.array(y)

# Vue qui va exécuter la prédiction
def predict_expenses_view(request, user_id):

     # Récupérer l'utilisateur
    try:
        user = Utilisateur.objects.get(id=user_id)
        entreprise_id = user.entreprise.id  # Supposant que 'entreprise' est la relation sur User
    except Utilisateur.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
    X, y = get_expenses_data(entreprise_id)
    
    if len(X) < 2:
        return JsonResponse({'error': 'Pas assez de données pour la régression.'})

    # Séparer les données en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer un modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prédire sur les données de test
    y_pred = model.predict(X_test)
    mse = np.mean((y_test - y_pred)**2)
    r2 = r2_score(y_test, y_pred)

    # Prédire pour la nouvelle période
    nouvelle_periode = np.array([[len(X)]])  # Index suivant
    prediction_nouvelle_periode = model.predict(nouvelle_periode)[0]

    # Retourner la prédiction et les évaluations sous forme de réponse JSON
    return JsonResponse({
        'mse': mse,
        'r2': r2,
        'prediction_nouvelle_periode': prediction_nouvelle_periode
    })
