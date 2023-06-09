from django.urls import path
from .views import( BanqueAPIView, BanqueDetail,DemandeAPIView,BanqueUpdate,CreateOffer, BanqueDelete, 
                   CLientAPIView, ClientDetail, ClientUpdate, ClientDelete, LoginView, OffreAPIView, OffreDetail, 
                   OffreUpdate, OffreDelete, CalculMensualite, CalculBenefice, CreationOffrePretView, RegisterView,
                   SoumettreDemandeView, AccepterDemandeView, RefuserDemandeView)

urlpatterns = [
    path('banques/', BanqueAPIView.as_view(), name='banque-api'),
    path('banques/<int:id>/', BanqueDetail.as_view(), name='banque-detail-api'),
    path('banques/<int:id>/update/', BanqueUpdate.as_view(), name='banque-update-api'),
    path('banques/<int:id>/delete/', BanqueDelete.as_view(), name='banque-delete-api'),

    ######### urls client 
    path('client/', CLientAPIView.as_view(), name='banque-api'),
    path('client/<int:id>/', ClientDetail.as_view(), name='banque-detail-api'),
    path('client/<int:id>/update/', ClientUpdate.as_view(), name='banque-update-api'),
    path('client/<int:id>/delete/', ClientDelete.as_view(), name='banque-delete-api'),

    ######### urls Offre 
    path('banques/<int:id_banque>/offers/', OffreAPIView.as_view(), name='banque-offers-api'),
    path('offer/', CreateOffer.as_view(), name='banque-offers-api'),
    path('offre/<int:id>/', OffreDetail.as_view(), name='banque-detail-api'),
    path('offre/<int:id>/update/', OffreUpdate.as_view(), name='banque-update-api'),
    path('offre/<int:id>/delete/', OffreDelete.as_view(), name='banque-delete-api'),

    ########## urls demandepret
    path('demande/', DemandeAPIView.as_view()),
    path('calcul-mensualite/', CalculMensualite.as_view(), name='calcul_mensualite'),
    path('calcul-Benefice/', CalculBenefice.as_view(), name='calcul_mensualite'),
    path('offre/', CreationOffrePretView.as_view(), name='calcul_mensualite'),
    path('demande/soumettre/', SoumettreDemandeView.as_view(), name='soumettre_demande'),

    ########## Authentification 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),


    ########### accepter ou refuser demande ####
    path('demandes/<int:demande_id>/accepter/', AccepterDemandeView.as_view(), name='accepter-demande'),
    path('demandes/<int:demande_id>/refuser/', RefuserDemandeView.as_view(), name='refuser-demande'),
    # Autres URL de votre application

]