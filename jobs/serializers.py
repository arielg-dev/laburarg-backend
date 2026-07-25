from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Traduce el modelo Job a JSON y viceversa.
    """

    # Por defecto, ModelSerializer mostraría el campo "company"
    # como un simple número (el ID de la empresa). Con
    # StringRelatedField, en cambio, mostramos directamente el
    # __str__ de la empresa relacionada (su nombre) -- mucho más
    # útil para el frontend, que así no necesita hacer una consulta
    # aparte solo para mostrar el nombre de la empresa en la tarjeta
    # de un aviso.
    company_name = serializers.StringRelatedField(source="company")

    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_name",
            "title",
            "description",
            "requirements",
            "province",
            "city",
            "modality",
            "contract_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]