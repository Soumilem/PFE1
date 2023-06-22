from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
#from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

from .manager import UserManager


# Create your models here.

Role = (
        ('Client', 'Client'),
        ('AdminBanque', 'AdminBanque'),
    )

class User(AbstractBaseUser,PermissionsMixin):
    nni = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    phone = models.CharField(max_length=16,unique=True)
    role = models.CharField(max_length=20, choices=Role, default="AdminBanque")
    is_active= models.BooleanField(default=True)
    verified= models.BooleanField(default=False)
    restricted= models.BooleanField(default=False)
    deleted= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_blocked= models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    
    REQUIRED_FIELDS = []

    def __str__(self) :
        return self.nom

@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
       if created:
            Token.objects.create(user= instance)

#User = get_user_model()


class Client(User):
    is_client = models.BooleanField(default=True)

class Banque(models.Model):
    nom_banque = models.CharField(max_length=100)
    #logo_banque = models.CharField(max_length=10)
    #num_telephone = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.nom_banque}"


class AdminBanque(User):
    is_admin = models.BooleanField(default=True)
    banque = models.OneToOneField(Banque, on_delete=models.CASCADE)



class CLientNNI(models.Model):
    NNI= models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    
    def __str__(self) :
        return  f"{self.NNI}"

class ClientBanque(models.Model):
     NNI = models.DecimalField(max_digits=10, decimal_places=0)
     num_compte = models.CharField(max_length=10, unique = True)
     banque = models.ForeignKey(Banque, on_delete=models.CASCADE)

    #  , related_name='client_banque'
     def __str__(self) :
        return  f"{self.num_compte}"

class Offers(models.Model):
    #demande_pret = models.ForeignKey(DemandePret, on_delete=models.CASCADE)
    banque = models.ForeignKey(Banque, on_delete=models.CASCADE)  # Utilisateur représentant la banque
    montant_emprunt = models.PositiveIntegerField(verbose_name="montant_emprunt")
    Interet = models.PositiveIntegerField(verbose_name="Taux d'intérêt (%)")
    duree_emprunt = models.PositiveIntegerField(verbose_name="Durée (mois)")
    mensualite = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    benefice_banque = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"Offre de {self.banque} - Montant: {self.montant_emprunt}MRU - Taux: {self.Interet}% - Durée: {self.duree_emprunt} mois"
    
class DemandePret(models.Model):
    STATUT_CHOICES = [
        ('attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    #raison = models.TextField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='attente')
    banque = models.ForeignKey(Banque, on_delete=models.SET_NULL, null=True, blank=True)
    offre = models.ForeignKey(Offers, on_delete=models.SET_NULL, null=True, blank=True)
    num_telephone = models.PositiveIntegerField()
    #num_compte = models.CharField(max_length=10, null=True)
    numero_compt = models.CharField(max_length=10)
    mensualite = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    duree_emprunt = models.PositiveIntegerField(null=True, blank=True)
    montant_emprunt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Salaire = models.DecimalField(max_digits=10, decimal_places=0)
    cni = models.FileField(upload_to="static/cni/")
    demande = models.FileField(upload_to='static/demande/')
    contrat_de_travail = models.FileField(upload_to='static/contrats_de_travail/')
    attestation_travail = models.FileField(upload_to='static/attestations_travail/')
    justification_adresse = models.FileField(upload_to='static/justifications_adresse/')
    bulletins_de_salaire = models.FileField(upload_to='static/bulletins_de_salaire/')
    montant_total=models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)


    def __str__(self):
        return f"Demande de prêt de {self.client} - Statut : {self.statut}"
    
    # def soumettre_demande(self, banque_id, offre_id):
    #     banque = get_object_or_404(Banque, id=banque_id)
    #     offre = Offers.objects.get(id=offre_id)

    #     self.banque = banque
    #     self.offre = offre
    #     self.statut = 'attente'
    #     self.save()
    

