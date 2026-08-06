from rest_framework import serializers

from .models import CV


class CandidateSerializer(serializers.ModelSerializer):
    """
    Vista de un CV pensada para que una EMPRESA lo consulte, no
    para que el propio usuario lo administre (para eso ya existe
    CVSerializer). Por eso expone campos distintos: acá sumamos
    algunos datos básicos del usuario dueño, pero deliberadamente
    NO incluimos su email ni teléfono -- el contacto directo debe
    darse a través de una postulación real, no de esta búsqueda
    exploratoria.
    """

    full_name = serializers.SerializerMethodField()
    province = serializers.CharField(source="user.province", read_only=True)
    city = serializers.CharField(source="user.city", read_only=True)

    class Meta:
        model = CV
        fields = [
            "id",
            "full_name",
            "province",
            "city",
            "title",
            "file",
            "uploaded_at",
        ]

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username