from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer específico para el registro de usuarios nuevos.

    Es un serializer DISTINTO al que usaríamos para, por ejemplo,
    mostrar el perfil de un usuario ya existente: acá necesitamos
    campos que no queremos exponer en otros contextos (la
    contraseña en texto plano, aunque sea solo de ENTRADA), y
    lógica de validación específica del registro.
    """

    # write_only=True: este campo se acepta en la entrada (cuando
    # alguien se registra), pero NUNCA se devuelve en ninguna
    # respuesta JSON de la API. Así evitamos que la contraseña
    # (aunque sea hasheada) viaje de vuelta al frontend sin
    # necesidad.
    #
    # validators=[validate_password]: reutiliza las mismas reglas
    # de seguridad que configuramos en AUTH_PASSWORD_VALIDATORS
    # (longitud mínima, que no sea muy común, que no sea solo
    # números, etc.) — las mismas que se aplican en el admin.
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "province",
            "city",
            "phone",
        ]

    def create(self, validated_data):
        """
        Sobreescribimos create() -- el método que ModelSerializer
        llama automáticamente al guardar un registro nuevo -- para
        controlar manualmente cómo se crea el usuario.

        Si no hiciéramos esto, ModelSerializer intentaría guardar
        el campo "password" tal cual, como texto plano, en la base
        de datos. Con create_user(), Django se encarga de hashearla
        correctamente antes de guardar.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        # set_password() hashea la contraseña. No usamos
        # user.password = password directamente, porque eso SÍ
        # guardaría el texto plano sin hashear.
        user.set_password(password)
        user.save()
        return user