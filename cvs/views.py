from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CV
from .serializers import CVSerializer


class CVViewSet(viewsets.ModelViewSet):
    """
    Expone las operaciones CRUD para CV, pero con dos reglas nuevas
    que no teníamos en CompanyViewSet ni JobViewSet:

    1. permission_classes = [IsAuthenticated]: nadie puede usar
       este endpoint sin mandar un access token válido.

    2. get_queryset() sobreescrito: en vez de devolver TODOS los
       CVs (como hacíamos con Company.objects.all()), devolvemos
       solo los del usuario que está haciendo el pedido. Así, un
       usuario logueado JAMÁS puede ver el CV de otra persona a
       través de esta API, ni siquiera cambiando el ID en la URL.
    """

    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # self.request.user es el usuario dueño del token que llegó
        # en el header Authorization. DRF ya lo identificó por
        # nosotros gracias a JWTAuthentication, que configuramos
        # como DEFAULT_AUTHENTICATION_CLASSES.
        return CV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Se ejecuta justo antes de guardar un CV nuevo. Como "user"
        # es read_only en el serializer (el frontend no lo manda),
        # lo completamos acá nosotros mismos con el usuario logueado.
        # Esto es lo que hace imposible que alguien suba un CV
        # "a nombre de otro usuario".
        serializer.save(user=self.request.user)