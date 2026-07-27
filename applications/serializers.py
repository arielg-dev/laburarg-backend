from rest_framework import serializers

from .models import Application, Favorite


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.StringRelatedField(source="job")

    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "job",
            "job_title",
            "cv",
            "status",
            "applied_at",
        ]
        # "status" también lo dejamos read_only desde el lado del
        # postulante: quien decide si una postulación pasa a
        # "vista", "rechazada" o "aceptada" es la empresa, no el
        # usuario que se postuló. Más adelante, cuando armemos
        # permisos para empresas, vamos a habilitar que ELLAS sí
        # puedan cambiar este campo.
        read_only_fields = ["user", "status", "applied_at"]


class FavoriteSerializer(serializers.ModelSerializer):
    job_title = serializers.StringRelatedField(source="job")

    class Meta:
        model = Favorite
        fields = ["id", "user", "job", "job_title", "created_at"]
        read_only_fields = ["user", "created_at"]