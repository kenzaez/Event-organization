from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractUser

class TypeRessource(models.TextChoices):
    MATERIEL = 'Materiel', 'Materiel'
    FOOD = 'Food', 'Food'

class TypeClient(models.TextChoices):
    INDIVIDU = 'Individu'
    ENTREPRISE = 'Entreprise'

class TypeEvenement(models.TextChoices):
    MARIAGE = 'Mariage'
    PARTY = 'Party'
    CONFERENCE = 'Conference'

class TypePaiement(models.TextChoices):
    ESPECE = 'Espece'
    CHEQUE = 'Cheque'
    VIREMENT = 'Virement'

class TypeFournisseur(models.TextChoices):
    MATERIEL = 'materiel'
    ENTERTAINMENT = 'entertainment'
    FOOD = 'Food'



class Client(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TypeClient.choices)
    num_tel = models.BigIntegerField()
    email = models.EmailField()
    adresse = models.TextField()
    deleted = models.BooleanField(default=False)
    image = models.ImageField(upload_to='client_images/', null=True, blank=True)
  
    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TypeFournisseur.choices)
    num_tel = models.BigIntegerField()
    email = models.EmailField()
    adresse = models.TextField()
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.nom

class Evenement(models.Model):
    date_evenement = models.DateField()
    type = models.CharField(max_length=20, choices=TypeEvenement.choices)
    date_contrat = models.DateField()
    status = models.CharField(max_length=100)
    Progress = models.DecimalField(max_digits=5, decimal_places=2,default="0.0")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ses_clients')
    fournisseurs = models.ManyToManyField(Fournisseur, related_name='ses_fournisseurs')
    deleted = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.date_evenement}"

class Paiement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="client")
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, null=True, blank=True, related_name='ses_paiements')
    type = models.CharField(max_length=20, choices=TypePaiement.choices)
    date_paiement = models.DateField()
    montant = models.FloatField()
    reste = models.FloatField()
    deadline = models.DateField()
class Ressource(models.Model):
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TypeRessource.choices)
    quantite_disponible = models.PositiveIntegerField(default=1)
    cout_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, related_name='ressources')
    returned = models.BooleanField(default=False)
    date_acquisition = models.DateField(null=True, blank=True)
    damaged = models.PositiveIntegerField(default=0)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='ressources', null=True, blank=True)
    @property
    def cout_total(self):
        if self.cout_unitaire is not None and self.quantite_disponible is not None and self.damaged == 0:
            return self.cout_unitaire * self.quantite_disponible
        elif  self.cout_unitaire is not None and self.quantite_disponible is not None and self.damaged == 0:
            return self.cout_unitaire * self.quantite_disponible + 50*self.damaged
        return 0.0  

    
   

