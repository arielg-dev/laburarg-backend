from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Application, Favorite
from .serializers import ApplicationSerializer, FavoriteSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Mismo patrón que CVViewSet: requiere login, y cada usuario solo
    ve/gestiona sus propias postulaciones.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)