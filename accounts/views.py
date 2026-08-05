from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer
from .tasks import send_welcome_email


class RegisterView(generics.CreateAPIView):
    """
    Endpoint de registro: POST /api/register/

    CreateAPIView es una vista genérica de DRF que expone
    ÚNICAMENTE la acción de crear (a diferencia de ModelViewSet,
    que trae las 5 operaciones CRUD completas).
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # .delay() es la forma más simple de "encolar" una tarea:
        # en vez de ejecutar send_welcome_email() directamente
        # (lo cual bloquearía este pedido HTTP hasta que el email
        # termine de mandarse), .delay() la manda a la cola de
        # Redis y sigue de largo INMEDIATAMENTE. El worker de
        # Celery la va a tomar y ejecutar por su cuenta, en paralelo.
        send_welcome_email.delay(user.id)