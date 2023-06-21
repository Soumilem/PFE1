from django.urls import path
from .views import *
urlpatterns = [
    path('banques/', BanqueAPIView.as_view(), name='banque-api'),
    path('banques/<int:id>/', BanqueDetail.as_view(), name='banque-detail-api'),
    path('banques/<int:id>/update/', BanqueUpdate.as_view(), name='banque-update-api'),
    path('banques/<int:id>/delete/', BanqueDelete.as_view(), name='banque-delete-api'),

    ######### urls client 
    path('numcompte/', ClientBanqueCreateAPIView.as_view()),
    path('enregistrer/', ClientCreateView.as_view()),
    path('client/', CLientAPIView.as_view(), name='banque-api'),
    path('client/<int:id>/', ClientDetail.as_view(), name='banque-detail-api'),
    path('client/<int:id>/update/', ClientUpdate.as_view(), name='banque-update-api'),
    path('client/<int:id>/delete/', ClientDelete.as_view(), name='banque-delete-api'),

    ######### urls Offre 
         ################# rescuperer les offres selon l'id du banque 
    path('banques/<int:id_banque>/offers/', OffreAPIView.as_view(), name='banque-offers-api'),
    #path('offer/', CreateOffer.as_view(), name='banque-offers-api'),
    path('offre/<int:id>/', OffreDetail.as_view(), name='banque-detail-api'),
    path('offre/<int:id>/update/', OffreUpdate.as_view(), name='banque-update-api'),
    path('offre/<int:id>/delete/', OffreDelete.as_view(), name='banque-delete-api'),

    ########## urls demandepret
    path('demande/', DemandeView.as_view()),
    path('demandes/', getdemande.as_view()),
    path('offre/', CreationOffrePretView.as_view(), name='calcul_mensualite'),
    path('demandeOffre/soumettre/', SoumettreDemandeView.as_view(), name='soumettre_demande'),

    ########## Authentification 
    path('register/client/', ClientRegisterView.as_view(), name='client-register'),
    path('register/banque/', AdminBanqueRegister.as_view(), name='banque-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    #path('register/', RegisterView.as_view(), name='register'),
    #path('login/', LoginView.as_view(), name='login'),


    ########### accepter ou refuser demande ####
    path('demandes/<int:demande_id>/accepter/', AccepterDemandeView.as_view(), name='accepter-demande'),
    path('demandes/<int:demande_id>/refuser/', RefuserDemandeView.as_view(), name='refuser-demande'),
    # Autres URL de votre application

]