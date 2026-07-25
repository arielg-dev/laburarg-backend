from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Traduce el modelo Company a JSON y viceversa.

    ModelSerializer es una clase de DRF que, a partir del modelo
    que le indiquemos, genera automáticamente los campos del
    serializer (mirando los campos del modelo), ahorrándonos
    escribirlos todos a mano uno por uno.
    """

    class Meta:
        model = Company
        # Los campos que van a viajar en el JSON. Usamos una lista
        # explícita (en vez de "__all__") a propósito: así, si más
        # adelante agregamos un campo sensible al modelo Company,
        # no se expone accidentalmente en la API sin que lo decidamos.
        fields = [
            "id",
            "name",
            "cuit",
            "is_agency",
            "verified",
            "website",
            "description",
            "created_at",
        ]
        # read_only_fields: campos que la API puede DEVOLVER pero
        # que nunca deberían poder ser modificados por quien manda
        # el JSON (por ejemplo, nadie debería poder "auto-verificarse"
        # mandando "verified": true en un POST).
        read_only_fields = ["verified", "created_at"]