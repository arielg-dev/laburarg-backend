from rest_framework import viewsets

from .models import Company, CompanyMember
from .permissions import IsCompanyMemberOrReadOnly
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

    Lectura pública, escritura solo para miembros de la empresa
    (ver IsCompanyMemberOrReadOnly).
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyMemberOrReadOnly]

    def perform_create(self, serializer):
        # Cuando alguien crea una empresa nueva, lo convertimos
        # automáticamente en su primer CompanyMember con rol OWNER.
        # Sin esto, la empresa quedaría creada pero SIN ningún
        # miembro -- y como nuestro permiso exige ser miembro para
        # editar, ¡ni su propio creador podría modificarla después!
        company = serializer.save()
        CompanyMember.objects.create(
            user=self.request.user,
            company=company,
            role=CompanyMember.Role.OWNER,
        )