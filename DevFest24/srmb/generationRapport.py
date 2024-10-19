from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Depenses , Utilisateur, Revenue,Passif,Actif
from django.db.models import Sum


def somme_depenses(idEntreprise, dateDebut, dateFin):
    

   # Récupérer toutes les dépenses correspondant aux critères
    depenses = Depenses.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin]
    ).values('date','type','description', 'montant')

    # Calculer la somme totale des dépenses
    total_depenses = depenses.aggregate(total=Sum('montant'))['total']

    # Si aucune dépense n'est trouvée, retourner 0 pour la somme
    if total_depenses is None:
        total_depenses = 0

    # Créer un tableau avec chaque date et montant
    tableau_depenses = [{'date': depense['date'], 'montant': depense['montant']} for depense in depenses]

    return total_depenses, tableau_depenses

#somme des revenues
def somme_revenues(idEntreprise, dateDebut, dateFin):
    

    # Calculer la somme des dépenses pour l'entreprise dans l'intervalle de dates donné
    total_revenues = Revenue.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin]
    ).values('date','categorie','description', 'montant')

# Calculer la somme totale des dépenses
    total_revenu = total_revenues.aggregate(total=Sum('montant'))['total']

    # Si aucune dépense n'est trouvée, retourner 0
    if total_revenu is None:
        total_revenu = 0

    # Créer un tableau avec chaque date et montant
    tableau_revenues = [{'date': depense['date'], 'montant': depense['montant']} for depense in total_revenues]
    

    return total_revenu,tableau_revenues

    #Compte de resultat
@csrf_exempt 
def generer_compteDeResultat(request, user_id):

    try:
        user = Utilisateur.objects.get(id=user_id)
        entreprise_id = user.entreprise.id  # Supposant que 'entreprise' est la relation sur User
    except Utilisateur.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
  

    if request.method == 'POST':
        try:
            # Récupérer le corps de la requête et extraire les dates
            body = json.loads(request.body)
            dateDebut = body.get('dateDebut')
            dateFin = body.get('dateFin')

            if not dateDebut or not dateFin:
                return JsonResponse({'error': 'Les dates dateDebut et dateFin sont obligatoires.'}, status=400)

            # Calculer la somme des revenues pour l'ID de l'entreprise dans l'intervalle donné
            total_depenses, tableau_dep=somme_depenses(entreprise_id, dateDebut, dateFin)
            total_revenues, tableau_revenues=somme_revenues(entreprise_id, dateDebut, dateFin)
            benefice_net=total_revenues-total_depenses
            return JsonResponse({'total_depenses': total_depenses, 'total_revenues':total_revenues, 'benefice_net':benefice_net, 'tableau_dep': tableau_dep, 'tableau_revenu':tableau_revenues})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Le corps de la requête doit être un JSON valide.'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée. Utilisez POST.'}, status=405)
    

       
 #somme des passifs    
def somme_passif(idEntreprise, dateDebut, dateFin):
    

    
    passifs = Passif.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin]
    ).values('code_operation','libellé','date', 'montant')

    total_passifs=passifs.aggregate(total=Sum('montant'))['total']
    if total_passifs is None:
        total_passifs = 0

# Créer un tableau avec chaque date et montant
    tableau_passifs = [{'date': depense['date'], 'montant': depense['montant']} for depense in passifs]

    return total_passifs, tableau_passifs

#somme des actifs
def somme_actif(idEntreprise, dateDebut, dateFin):
    

   
    actifs = Actif.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin]
    ).values('code_operation','libellé','date', 'montant')

    total_actifs=actifs.aggregate(total=Sum('montant'))['total']

    if total_actifs is None:
        total_actifs = 0

# Créer un tableau avec chaque date et montant
    tableau_actifs = [{'date': depense['date'], 'montant': depense['montant']} for depense in actifs]

    return total_actifs,tableau_actifs

#Bilans
@csrf_exempt 
def generer_bilan(request, user_id):

    try:
        user = Utilisateur.objects.get(id=user_id)
        entreprise_id = user.entreprise.id  # Supposant que 'entreprise' est la relation sur User
    except Utilisateur.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
  

    if request.method == 'POST':
        try:
            # Récupérer le corps de la requête et extraire les dates
            body = json.loads(request.body)
            dateDebut = body.get('dateDebut')
            dateFin = body.get('dateFin')

            if not dateDebut or not dateFin:
                return JsonResponse({'error': 'Les dates dateDebut et dateFin sont obligatoires.'}, status=400)

            
            total_passif, tableau_passif=somme_passif(entreprise_id, dateDebut, dateFin)
            total_actif, tableau_actif=somme_actif(entreprise_id, dateDebut, dateFin)
            capitaux_propres=total_actif-total_passif
            return JsonResponse({'total_passif': total_passif, 'total_actif':total_actif, 'capitaux_propres':capitaux_propres, 'tableau_passif':tableau_passif,'tableau_actif':tableau_actif})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Le corps de la requête doit être un JSON valide.'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée. Utilisez POST.'}, status=405)
  

  #flux de tresories depenses 
  
def somme_depenses_flux(idEntreprise, dateDebut, dateFin, typeFlux):
    

    # Calculer la somme des dépenses avec le type de flux 'opérationnelle'
    tab_depenses = Depenses.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin],
        type_flux_tresorerie=typeFlux  # Filtre par type de flux
    ).values('date','type_flux_tresorerie', 'montant')

# Calculer la somme totale des dépenses
    total_depenses = tab_depenses.aggregate(total=Sum('montant'))['total']

# Créer un tableau avec chaque date et montant
    tableau_depenses = [{'date': depense['date'], 'montant': depense['montant']} for depense in tab_depenses]

    # Si aucune dépense n'est trouvée, retourner 0
    if total_depenses is None:
        total_depenses = 0

    return total_depenses, tableau_depenses

#flux de tresories revenus 
  
def somme_revenu_flux(idEntreprise, dateDebut, dateFin, typeFlux):
    

    # Calculer la somme des dépenses avec le type de flux 'opérationnelle'
    tab_depenses = Revenue.objects.filter(
        entreprise_id=idEntreprise,
        date__range=[dateDebut, dateFin],
        type_flux_tresorerie=typeFlux  # Filtre par type de flux
    ).values('date','type_flux_tresorerie', 'montant')

# Calculer la somme totale des dépenses
    total_depenses = tab_depenses.aggregate(total=Sum('montant'))['total']

# Créer un tableau avec chaque date et montant
    tableau_depenses = [{'date': depense['date'], 'montant': depense['montant']} for depense in tab_depenses]

    # Si aucune dépense n'est trouvée, retourner 0
    if total_depenses is None:
        total_depenses = 0

    return total_depenses, tableau_depenses


#Flux de tresorie
@csrf_exempt 
def generer_flux_de_tresorie(request, user_id):

    try:
        user = Utilisateur.objects.get(id=user_id)
        entreprise_id = user.entreprise.id  # Supposant que 'entreprise' est la relation sur User
    except Utilisateur.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
  

    if request.method == 'POST':
        try:
            # Récupérer le corps de la requête et extraire les dates
            body = json.loads(request.body)
            dateDebut = body.get('dateDebut')
            dateFin = body.get('dateFin')

            if not dateDebut or not dateFin:
                return JsonResponse({'error': 'Les dates dateDebut et dateFin sont obligatoires.'}, status=400)

            
            total_depenses_oper, tab_dep_op=somme_depenses_flux(entreprise_id, dateDebut, dateFin, "opérationnelle")
            total_depenses_invest, tab_dep_invest=somme_depenses_flux(entreprise_id, dateDebut, dateFin, "investissement")
            total_depenses_finan, tab_dep_finan=somme_depenses_flux(entreprise_id, dateDebut, dateFin, "financement")

            total_revenu_oper,tab_revenu_oper=somme_revenu_flux(entreprise_id, dateDebut, dateFin, "opérationnelle")
            total_revenu_invest,tab_revenu_invest=somme_revenu_flux(entreprise_id, dateDebut, dateFin, "investissement")
            total_revenu_finan,tab_revenu_finan=somme_revenu_flux(entreprise_id, dateDebut, dateFin, "financement")
           
            activité_opérationelles= total_revenu_oper-total_depenses_oper
            activité_investissement= total_revenu_invest-total_depenses_invest
            activité_financement= total_revenu_finan-total_depenses_finan
            
            return JsonResponse({' activité_opérationelles':  activité_opérationelles, 'activité_investissement':activité_investissement, 'activité_financement':activité_financement})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Le corps de la requête doit être un JSON valide.'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée. Utilisez POST.'}, status=405)
  
