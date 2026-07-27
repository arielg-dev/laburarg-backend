from rest_framework import serializers

from .models import CV


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = [
            "id",
            "user",
            "title",
            "file",
            "is_primary",
            "uploaded_at",
        ]
        # "user" no lo va a mandar el frontend: lo vamos a asignar
        # nosotros automáticamente en el ViewSet, a partir de quién
        # esté logueado (el dueño del token). Por eso es read_only:
        # la API lo devuelve en las respuestas, pero ignora
        # cualquier valor que alguien intente mandar para ese campo.
        read_only_fields = ["user", "uploaded_at"]