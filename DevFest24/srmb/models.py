from django.db import models

# Modèle pour la table Entreprise
class Entreprise(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Modèle pour la table Actif
class Actif(models.Model):
    TYPE_CHOICES = (
        ('liquide', 'Liquide'),
        ('stocks', 'Stocks'),
    )
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='actifs')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    code_operation=models.DecimalField(max_digits=15, decimal_places=2)
    libellé = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.type} - {self.montant}"

# Modèle pour la table Passif
class Passif(models.Model):
    TYPE_CHOICES = (
        ('emprunts', 'Emprunts'),
        ('dattes', 'Dattes'),
        ('fournisseur', 'Fournisseur'),
        ('autre', 'Autre'),
    )
    libellé = models.CharField(max_length=255)
    code_operation=models.DecimalField(max_digits=15, decimal_places=2)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='passifs')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.type} - {self.montant}"

# Modèle pour la table Depenses
class Depenses(models.Model):
    TYPE_CHOICES = (
        ("Dépenses d'exploitation", "Dépenses d'exploitation"),
        ("Salaires", "Salaires"),
        ("Loyer", "Loyer"),
        ("Impôts et taxes", "Impôts et taxes"),
        ("Dépenses financières", "Dépenses financières"),
        ("autre", "Autre"),
    )
    TYPE_FLUX_CHOICES = (
        ('opérationnelle', 'Opérationnelle'),
        ('investissement', 'Investissement'),
        ('financement', 'Financement'),
    )
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='depenses')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    type_flux_tresorerie = models.CharField(max_length=50, choices=TYPE_FLUX_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.montant}"

# Modèle pour la table Revenue
class Revenue(models.Model):
    CATEGORIE_CHOICES = (
        ('Vente', 'Vente'),
        ('Service', 'Service'),
        ('Autre', 'Autre'),
    )
    TYPE_FLUX_CHOICES = (
        ('opérationnelle', 'Opérationnelle'),
        ('investissement', 'Investissement'),
        ('financement', 'Financement'),
    )
    type_flux_tresorerie = models.CharField(max_length=50, choices=TYPE_FLUX_CHOICES)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='revenues')
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.categorie} - {self.montant}"

# Modèle pour la table Utilisateur
class Utilisateur(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
    )
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='utilisateurs')
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Pensez à utiliser le hachage de mot de passe via User model
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



class Recommendation(models.Model):
    enterprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='recommandations')
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommandation pour {self.enterprise.name}"
