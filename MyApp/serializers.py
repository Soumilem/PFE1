from rest_framework import serializers
from .models import Banque, Client, DemandePret, Offers


class BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class DemandePretSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandePret
        fields = ['client','banque','num_telephone', 'num_compte','duree_emprunt','montant_emprunt', 'Salaire', 'cni', 'demande', 'contrat_de_travail', 'attestation_travail',
                  'justification_adresse', 'bulletins_de_salaire']


class DemandePretWithOffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandePret
        fields = ['client','banque','offre','num_telephone', 'num_compte', 'Salaire', 'cni', 'demande', 'contrat_de_travail', 'attestation_travail',
                  'justification_adresse', 'bulletins_de_salaire'] 

class OffreSerializer(serializers.ModelSerializer):
    banque = serializers.StringRelatedField()
    class Meta:
        model = Offers
        fields = '__all__'

class PretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ['banque', 'montant_emprunt','Interet','duree_emprunt']

    