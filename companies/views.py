from rest_framework import viewsets

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Expone las operaciones CRUD para Company vía API REST.

    ModelViewSet nos da, gratis, las siguientes acciones:
    - GET    /api/companies/        -> listar todas las empresas
    - POST   /api/companies/        -> crear una empresa nueva
    - GET    /api/companies/{id}/   -> ver una empresa puntual
    - PUT    /api/companies/{id}/   -> reemplazar una empresa
    - PATCH  /api/companies/{id}/   -> editar parcialmente
    - DELETE /api/companies/{id}/   -> borrar una empresa

    Todo esto sin escribir ninguna de esas funciones a mano.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer