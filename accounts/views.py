from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Endpoint de registro: POST /api/register/

    CreateAPIView es una vista genérica de DRF que expone
    ÚNICAMENTE la acción de crear (a diferencia de ModelViewSet,
    que trae las 5 operaciones CRUD completas). Tiene sentido acá:
    no existe "listar todos los registros" como concepto de
    negocio, solo "crear una cuenta nueva".
    """

    serializer_class = RegisterSerializer

    # AllowAny: a diferencia de CVViewSet o ApplicationViewSet,
    # este endpoint tiene que ser accesible SIN estar logueado --
    # tiene sentido, nadie puede loguearse antes de tener una
    # cuenta. Lo hacemos explícito para que quede claro que es una
    # decisión consciente, no un permiso que nos olvidamos de poner.
    permission_classes = [AllowAny]