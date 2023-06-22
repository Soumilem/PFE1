from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

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
        fields = ['banque_id','logo_banque','num_telephone','username', 'password']

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
        fields = ['client','banque','num_telephone', 'numero_compt','duree_emprunt','montant_emprunt', 'Salaire', 'cni', 'demande', 'contrat_de_travail', 'attestation_travail',
                  'justification_adresse', 'bulletins_de_salaire']

class DemandePretWithOffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandePret
        fields = ['client','banque','offre','num_telephone', 'numero_compt', 'Salaire', 'cni', 'demande', 'contrat_de_travail', 'attestation_travail',
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
  
class enregistrerserializer(serializers.ModelSerializer):
    class Meta:
        model = CLientNNI
        fields = '__all__'

class ClientBanqueSerializer(serializers.ModelSerializer):
    nni = enregistrerserializer()

    class Meta:
        model = ClientBanque
        fields = ['nni', 'num_compte', 'banque_id']

class test(serializers.ModelSerializer):
    class Meta:
        model = ClientBanque
        fields = '__all__'


# class AdminBanqueSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=150)
#     password = serializers.CharField(write_only=True)
#     nom_banque  =serializers.CharField(write_only=True)
#     class Meta:
#         model = AdminBanque
#         fields = ['num_telephone','username', 'password', 'banque_id']

#     def create(self, validated_data):
#         username = validated_data.pop('username')
#         password = validated_data.pop('password')
#         banque_id = validated_data.pop('banque_id')
#         banque = Banque.objects.get(id= banque_id)
#         user.is_admin=True
#         user = User.objects.create_user(username=username, password=password)
#         adminbnq = Banque.objects.create(user=user,banque=banque, **validated_data)
#         return adminbnq
    

class ResponsableBanqueSerializer(serializers.ModelSerializer):
    banque_id = serializers.PrimaryKeyRelatedField(queryset=Banque.objects.all(), source='banque')
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AdminBanque
        fields = ['nni', 'nom', 'prenom', 'num_telephone', 'banque_id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        banque_id = validated_data.pop('banque_id')
        user.is_admin=True
        user = User.objects.create_user(username=username, password=password)
        admin_banque = AdminBanque.objects.create(user=user, banque=banque_id, **validated_data)
        return admin_banque


class MyTokenObtainPairManagerSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        
        try:
            obj= AdminBanque.objects.get(phone=data['phone'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Informations invalides.'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})





class RegisterManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBanque
        fields = ('id', 'phone', 'nom', 'password','role','banque')
        extra_kwargs = {
            'password': {'write_only': True}
        }

## register vendor
class RegisterVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone', 'nom', 'password','role')
        extra_kwargs = {
            'password': {'write_only': True}
        }