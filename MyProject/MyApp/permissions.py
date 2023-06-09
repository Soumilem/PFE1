from rest_framework.permissions import BasePermission, IsAdminUser
class Is_Client(BasePermission):
    def has_permission(self, request, view):
        # Vérifiez ici les conditions spécifiques pour l'autorisation de l'utilisateur de type 1
        return bool(request.user and request.user.is_client)
    


class Is_AdminBanque(BasePermission):
    def has_permission(self, request, view):
        # Vérifiez ici les conditions spécifiques pour l'autorisation de l'utilisateur de type 2
        return bool(request.user and request.user.is_admin)
    
class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        # Autorise les opérations en lecture (GET, HEAD, OPTIONS) pour tout le monde
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return super().has_permission(request, view)
