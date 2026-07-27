from rest_framework import viewsets

from companies.permissions import IsJobCompanyMemberOrReadOnly

from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    Expone las operaciones CRUD para Job vía API REST.

    Lectura pública, escritura solo para miembros de la empresa
    dueña del aviso.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsJobCompanyMemberOrReadOnly]

    filterset_fields = ["province", "modality", "contract_type", "status"]