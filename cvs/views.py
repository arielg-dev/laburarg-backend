from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .candidate_serializers import CandidateSerializer
from .models import CV
from .permissions import HasCVDatabaseAccess
from .serializers import CVSerializer


class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CandidateSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Búsqueda de candidatos para empresas con suscripción paga.

    ReadOnlyModelViewSet: a diferencia de ModelViewSet, solo
    expone "list" (GET /api/candidates/) y "retrieve"
    (GET /api/candidates/{id}/) -- ninguna operación de escritura,
    porque no tiene sentido que una empresa modifique el CV de
    otro usuario.
    """

    queryset = CV.objects.select_related("user").all()
    serializer_class = CandidateSerializer
    permission_classes = [HasCVDatabaseAccess]
    filterset_fields = ["is_primary"]