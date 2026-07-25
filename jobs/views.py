from rest_framework import viewsets

from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    Expone las operaciones CRUD para Job vía API REST.

    Por ahora devolvemos TODOS los jobs (incluidos borradores).
    Cuando lleguemos al bloque de permisos, vamos a filtrar esto
    para que el público solo vea los que tengan status="active",
    y que una empresa pueda ver sus propios borradores.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer

    # DRF permite filtrar resultados vía parámetros en la URL.
    # Esto habilita, por ejemplo:
    # GET /api/jobs/?province=Córdoba
    # GET /api/jobs/?modality=hybrid
    filterset_fields = ["province", "modality", "contract_type", "status"]