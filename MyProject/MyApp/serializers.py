from rest_framework import serializers
from .models import Banque, Client, DemandePret, Offers, User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'is_client', 'is_admin')

class ClientRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['nni', 'nom', 'prenom', 'num_telephone','username', 'password']


    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(username=username, password=password)
        
        client = Client.objects.create(user=user, **validated_data)
        return client



class AdminBanqueregisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Banque
        fields = ['nom_banque','logo_banque','num_telephone','username', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user.is_admin=True
        user = User.objects.create_user(username=username, password=password)
        adminbnq = Banque.objects.create(user=user, **validated_data)
        return adminbnq
    


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
        fields = ['montant_emprunt','Interet','duree_emprunt']

    