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
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Banque, Client, DemandePret, Offers, User
from .serializers import BanqueSerializer, DemandePretSerializer, PretSerializer,ClientSerializer, OffreSerializer, DemandePretWithOffreSerializer
# Create your views here.

########################## Banque API ##################

class BanqueAPIView(APIView):
    def get(self, request):
        banques = Banque.objects.all()
        serializer = BanqueSerializer(banques, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = BanqueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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

class OffreAPIView(APIView):
    def get(self, request, banque_id):
        try:
            banque = Banque.objects.get(id=banque_id)
        except Banque.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        offers = Offers.objects.filter(banque=banque)
        serializer = OffreSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OffreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateOffer(APIView):
    def post(self, request):
        serializer = OffreSerializer(data=request.data)
        if serializer.is_valid():
            id_banque = request.data.get('banque')
            try:
                banque = Banque.objects.get(id=id_banque)
            except Banque.DoesNotExist:
                return Response({"message": "La banque spécifiée n'existe pas."}, status=status.HTTP_404_NOT_FOUND)

            offer = serializer.save(banque=banque)
            response_data = {
                "message": "L'offre a été créée avec succès.",
                "offer_id": offer.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OffreDetail(APIView):
    def get(self, request, id):
        try:
            offre = Offers.objects.get(id=id)
        except Offers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BanqueSerializer(offre)
        return Response(serializer.data)


class OffreUpdate(APIView):
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
    def delete(self, request, id):
        try:
            offre = Offers.objects.get(id=id)
        except Offers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        offre.delete()




######################### API DemandePret #########


class DemandeAPIView(APIView):

 def post(self, request):
        serializer = DemandePretWithOffreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Demande soumise avec succès', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 def post(self, request):
        serializer = DemandePretSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Demande soumise avec succès', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 def get(self, request):
        banques = DemandePret.objects.all()
        serializer = DemandePretWithOffreSerializer(banques, many=True)
        return Response(serializer.data)

 

 
 


 ############################## Calcuel de mensualite ##############################

class CalculMensualite(APIView):
  def post(self, request):
        serializer = PretSerializer(data=request.data)
        if serializer.is_valid():
            pret = serializer.validated_data['montant_emprunt']
            taux = serializer.validated_data['Interet']
            duree = serializer.validated_data['duree_emprunt']

            taux = taux / 100 / 12  # Conversion du taux d'intérêt annuel en taux mensuel
            duree = duree * 12  # Conversion de la durée en mois

            mensualite = (pret * taux) / (1 - (1 + taux) ** -duree)

            return Response({'mensualite': mensualite}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class CalculBenefice(APIView):
    def post(self, request):
        serializer = PretSerializer(data=request.data)
        if serializer.is_valid():
            pret = serializer.validated_data['montant_emprunt']
            taux = serializer.validated_data['Interet']
            duree = serializer.validated_data['duree_emprunt']

            taux = taux / 100  # Conversion du taux d'intérêt en décimal
            montant_total = pret * (1 + taux * duree)  # Calcul du montant total remboursé (principal + intérêts)

            benefice = montant_total - pret  # Calcul du bénéfice (montant total remboursé - montant initial du prêt)

            return Response({'benefice': montant_total}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



###################################### pour test #########################
# class CreationOffrePretView(APIView):
#     def post(self, request):
#         serializer = PretSerializer(data=request.data)
#         if serializer.is_valid():
#             banque = serializer.validated_data['banque']
#             montant_emprunt = serializer.validated_data['montant_emprunt']
#             taux_interet = serializer.validated_data['Interet']
#             duree_emprunt = serializer.validated_data['duree_emprunt']

#             # Appel à la fonction de calcul de la mensualité
#             taux_mensuel = taux_interet / 100 / 12
#             duree_mois = duree_emprunt
#             mensualite = (montant_emprunt * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_mois)

#             # Appel à la fonction de calcul du bénéfice
#             montant_total = montant_emprunt * (1 + taux_mensuel * duree_mois)
#             benefice = montant_total - montant_emprunt

#             # Création de l'offre de prêt avec les attributs calculés
#             offre = serializer.save(mensualite=mensualite, benefice_banque=benefice)

#             return Response({
#                 'banque': offre.banque,
#                 'montant_emprunt': offre.montant_emprunt,
#                 'Interet': offre.Interet,
#                 'duree_emprunt': offre.duree_emprunt,
#                 'mensualite': offre.mensualite,
#                 'benefice_banque': offre.benefice_banque
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreationOffrePretView(APIView):
    def post(self, request):
        serializer = PretSerializer(data=request.data)
        if serializer.is_valid():
            montant_emprunt = serializer.validated_data['montant_emprunt']
            taux_interet = serializer.validated_data['Interet']
            duree_emprunt = serializer.validated_data['duree_emprunt']
            banque_id = request.data['banque']  # Supposons que l'ID de la banque est passé dans la requête

            # Appel à la fonction de calcul de la mensualité
            taux_mensuel = taux_interet / 100 / 12
            duree_mois = duree_emprunt
            mensualite = (montant_emprunt * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_mois)

            # Appel à la fonction de calcul du bénéfice
            montant_total = montant_emprunt * (1 + taux_mensuel * duree_mois)
            benefice = montant_total - montant_emprunt

            # Récupération de l'instance de la banque
            banque = get_object_or_404(Banque, id=banque_id)

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
        




############################# soumettre en demande ###############
class SoumettreDemandeView(APIView):
    #@login_required
    def post(self, request):
        #permission_classes = [AllowAny]
        permission_classes = [IsAuthenticated]


        banque_id = request.data.get('banque_id')
        offre_id = request.data.get('offre_id')
        #client = get_object_or_404(Client, user=request.user)

        if request.user.is_authenticated:
          demande = DemandePret(
            client = request.user.client,  # Récupérer le client associé à l'utilisateur connecté
            raison=request.data.get('raison'),
            num_telephone=request.data.get('num_telephone'),
            num_compte=request.data.get('num_compte'),
            Salaire=request.data.get('Salaire'),
            cni=request.FILES.get('cni'),
            demande=request.FILES.get('demande'),
            contrat_de_travail=request.FILES.get('contrat_de_travail'),
            attestation_travail=request.FILES.get('attestation_travail'),
            justification_adresse=request.FILES.get('justification_adresse'),
            bulletins_de_salaire=request.FILES.get('bulletins_de_salaire'),
          )

          demande.soumettre_demande(banque_id=banque_id, offre_id=offre_id)

          return Response({'message': 'Demande soumise avec succès'})
        return Response({'message': 'user non autentifi'})




################################# Authentification #######################

class RegisterView(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         num_telephone = request.data.get('num_telephone')
#         password = request.data.get('password')
#         user = authenticate(num_telephone=num_telephone,password=password)
#         if user.check_password(password):
#             refresh_token = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'refresh': str(refresh_token),
#                 'access': str(refresh_token.access_token),
#             })
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            })
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
