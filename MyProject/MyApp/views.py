from imaplib import _Authenticator
from django import views
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from MyApp.permissions import Is_Client, Is_AdminBanque
from .models import Banque, Client, DemandePret, Offers, User
from .serializers import (BanqueSerializer, DemandePretSerializer, PretSerializer,ClientSerializer, OffreSerializer,
                           DemandePretWithOffreSerializer, ClientRegisterSerializer, 
                           AdminBanqueregisterSerializer, enregistrerserializer)
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from rest_framework.exceptions import ValidationError

# Create your views here.


########################## Banque API ##################

class BanqueAPIView(APIView):
    permission_classes = [IsAuthenticated&Is_Client]
    def get(self, request):
        banques = Banque.objects.all()
        serializer = BanqueSerializer(banques, many=True)
        return Response(serializer.data)

class BanqueDetail(APIView):
    def get(self, request, id):
        try:
            banque = Banque.objects.get(id=id)
        except Banque.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BanqueSerializer(banque)
        return Response(serializer.data)


class BanqueUpdate(APIView):
    def put(self, request, id):
        try:
            banque = Banque.objects.get(id=id)
        except Banque.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BanqueSerializer(banque, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BanqueDelete(APIView):
    def delete(self, request, id):
        try:
            banque = Banque.objects.get(id=id)
        except Banque.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        banque.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


########################## Client API ##################

class CLientAPIView(APIView):
    permission_classes =[IsAdminUser]
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientRegisterSerializer(client, many=True)
        return Response(serializer.data)

    
class ClientDetail(APIView):
    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class ClientUpdate(APIView):
    def put(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDelete(APIView):
    def delete(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################## Offre API ##################

class CreationOffrePretView(APIView):
    permission_classes = [IsAuthenticated&Is_AdminBanque]

    def post(self, request):
        serializer = PretSerializer(data=request.data)
        if serializer.is_valid():
            montant_emprunt = serializer.validated_data['montant_emprunt']
            taux_interet = serializer.validated_data['Interet']
            duree_emprunt = serializer.validated_data['duree_emprunt']

            # Obtention de la banque à partir de l'utilisateur authentifié
            banque = request.user.banque

            # Vérification si l'offre existe déjà dans la banque
            if Offers.objects.filter(banque=banque).exists():
                raise ValidationError("Une offre existe déjà pour cette banque.")

           
             # Appel à la fonction de calcul de la mensualité
            taux_mensuel = taux_interet / 100 / 12
            duree_mois = duree_emprunt
            mensualite = (montant_emprunt * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_mois)

            # Appel à la fonction de calcul du bénéfice
            montant_total = montant_emprunt * (1 + taux_mensuel * duree_mois)
            benefice = montant_total - montant_emprunt

             # Création de l'offre de prêt avec les attributs calculés et la banque associée
            offre = Offers.objects.create(
                 banque=banque,
                 montant_emprunt=montant_emprunt,
                 Interet=taux_interet,
                 duree_emprunt=duree_emprunt,
                 mensualite=mensualite,
                 benefice_banque=montant_total
             )

            return Response({
                'montant_emprunt': offre.montant_emprunt,
                'Interet': offre.Interet,
                'duree_emprunt': offre.duree_emprunt,
                'mensualite': offre.mensualite,
                'benefice_banque': offre.benefice_banque
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OffreAPIView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request, banque_id):
        try:
            banque = Banque.objects.get(id=banque_id)
        except Banque.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        offers = Offers.objects.filter(banque=banque)
        serializer = OffreSerializer(offers, many=True)
        return Response(serializer.data)
       
class OffreDetail(APIView):
    permission_classes =[IsAuthenticated &Is_AdminBanque]
    def get(self, request, id):
        try:
            offre = Offers.objects.get(id=id)
        except Offers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BanqueSerializer(offre)
        return Response(serializer.data)


class OffreUpdate(APIView):
    permission_classes = [IsAuthenticated&Is_AdminBanque]
    def put(self, request, id):
        try:
            offre = Offers.objects.get(id=id)
        except Offers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OffreSerializer(offre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OffreDelete(APIView):
    permission_classes = [IsAuthenticated&Is_AdminBanque]
    def delete(self, request, id):
        try:
            offre = Offers.objects.get(id=id)
        except Offers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        offre.delete()




######################### API DemandePret #########

class demnd(APIView):
    permission_classes =[IsAuthenticated&Is_AdminBanque]
    def get(self, request):
        # Récupérer l'utilisateur authentifié (la banque)
        banque = request.user.banque
        # Récupérer les demandes de prêt soumises à cette banque
        demandes = DemandePret.objects.filter(banque=banque)

        # Sérialiser les demandes
        demandes_serializer = DemandePretWithOffreSerializer(demandes, many=True)

        return Response(demandes_serializer.data)

class DemandeAPIView(APIView):
 permission_classes =[IsAuthenticated&Is_AdminBanque]
 class DemandesPretView(APIView):
    def get(self, request):
        # Récupérer toutes les demandes de prêt
        demandes = DemandePret.objects.all()

        # Sérialiser les demandes
        demandes_serializer = DemandePretSerializer(demandes, many=True)

        return Response(demandes_serializer.data)

 permission_classes =[IsAuthenticated&Is_Client]
 def post(self, request):
        serializer = DemandePretWithOffreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Demande soumise avec succès', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 permission_classes =[IsAuthenticated&Is_Client]
 def post(self, request):
        serializer = DemandePretSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Demande soumise avec succès', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 permission_classes =[IsAuthenticated]
 def get(self, request):
        banques = DemandePret.objects.all()
        serializer = DemandePretWithOffreSerializer(banques, many=True)
        return Response(serializer.data)

############################# soumettre en demande ###############



class DemandeAPI(APIView):
    def post(self, request):
        # Récupérer les critères de sélection de la banque depuis la requête
        criteres_banque = request.data.get('criteres_banque')

        # Effectuer la recherche de la banque en fonction des critères
        banques = Banque.objects.filter(**criteres_banque)

        # Sérialiser les résultats de la sélection de la banque
        banque_serializer = BanqueSerializer(banques, many=True)
        
        # Récupérer l'identifiant de la banque sélectionnée depuis la requête
        banque_id = request.data.get('banque_id')

        # Récupérer les offres de la banque sélectionnée
        offres = Offers.objects.filter(banque=banque_id)

        # Sérialiser les résultats de la sélection des offres
        offre_serializer = OffreSerializer(offres, many=True)

        # Sérialiser les données de la demande
        demande_serializer = DemandePretSerializer(data=request.data.get('donnees_personnelles'))

        if banque_serializer.is_valid() and offre_serializer.is_valid() and demande_serializer.is_valid():
            # Sauvegarder la demande dans la base de données
            demande = demande_serializer.save()

            # Ajouter les offres sélectionnées à la demande
            demande.offres.set(offres)

            return Response({
                'banques': banque_serializer.data,
                'offres': offre_serializer.data,
                'demande': demande_serializer.data
            }, status=201)
        
        return Response({
            'errors': {
                'banque_errors': banque_serializer.errors,
                'offre_errors': offre_serializer.errors,
                'demande_errors': demande_serializer.errors
            }
        }, status=400)
class SoumettreDemandeView(APIView):
    permission_classes = [IsAuthenticated&Is_Client]
    def post(self, request):
        banque_id = request.data.get('banque_id')
        offre_id = request.data.get('offre_id')

        if request.user.is_authenticated:
          demande = DemandePret(
            client = request.user.client,  # Récupérer le client associé à l'utilisateur connecté
            num_telephone=request.data.get('num_telephone'),
            numero_compt=request.data.get('numero_compt'),
            Salaire=request.data.get('Salaire'),
            cni=request.FILES.get('cni'),
            demande=request.FILES.get('demande'),
            contrat_de_travail=request.FILES.get('contrat_de_travail'),
            attestation_travail=request.FILES.get('attestation_travail'),
            justification_adresse=request.FILES.get('justification_adresse'),
            bulletins_de_salaire=request.FILES.get('bulletins_de_salaire'),
          )

          demande.soumettre_demande(banque_id=banque_id, offre_id=offre_id)

          return Response({'message': 'Demande soumise avec succès',
                'banque': demande.banque,
                'offre': demande.offre,
                'num_telephone': demande.num_telephone,
                'numero_compt': demande.numero_compt,
                'Salaire': demande.Salaire,
                'cni': demande.cni,
                'demandeecrit': demande.demande,
                'contrat_de_travail': demande.contrat_de_travail,
                'attestation_travail': demande.attestation_travail,
                'justification_adresse': demande.justification_adresse,
                'bulletins_de_salaire': demande.bulletins_de_salaire,
                }, status=status.HTTP_201_CREATED)
        return Response({'message': 'user non autentifi'})

######################### accepter demande ###########

class AccepterDemandeView(APIView):
    def put(self, request, demande_id):
        banque = get_object_or_404(Banque, AdminBanque=request.user)
        demande = get_object_or_404(DemandePret, id=demande_id, banque=banque, statut='attente')

        demande.statut = 'approuvee'
        demande.save()

        return Response({'message': 'La demande a été acceptée.'})

class RefuserDemandeView(APIView):
    def put(self, request, demande_id):
        banque = get_object_or_404(Banque, AdminBanque=request.user)
        demande = get_object_or_404(DemandePret, id=demande_id, banque=banque, statut='attente')

        demande.statut = 'rejetee'
        demande.save()

        return Response({'message': 'La demande a été refusée.'})


#####################################
class ClientRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            @receiver(post_save, sender=User)
            def set_user_as_client(sender, instance, created, **kwargs):
                 if created:
                   instance.is_client = True
                   instance.save()
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            client = Client.objects.create(
                user=user,
                nni=serializer.validated_data['nni'],
                nom=serializer.validated_data['nom'],
                prenom=serializer.validated_data['prenom'],
                num_telephone=serializer.validated_data['num_telephone']
            )
            return Response({'message': 'Client registered successfully.'})
        return Response(serializer.errors)
    

#################################### register AdminBanque ######################################    

class AdminBanqueRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminBanqueregisterSerializer(data=request.data)
        if serializer.is_valid():
            @receiver(post_save, sender=User)
            def set_user_as_admin(sender, instance, created, **kwargs):
             if created:
               instance.is_admin = True
               instance.save()
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            


            admin_banque = Banque.objects.create(
                user=user,
                #nom=serializer.validated_data['nom'],
                #prenom=serializer.validated_data['prenom'],
                num_telephone=serializer.validated_data['num_telephone'],
                nom_banque=serializer.validated_data['nom_banque'],
                logo_banque=serializer.validated_data['logo_banque']
            )
            #user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors)

######################################## login ########################################

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        return Response({'error': 'Invalid credentials.'})
    
################################# enregistrer nni dans base de donnes #######################


class ClientCreateView(APIView):
    def post(self, request):
        serializer = enregistrerserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)










