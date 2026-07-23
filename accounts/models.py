from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuario personalizado para LaburArg.

    Heredamos de AbstractUser en vez de escribir un modelo desde cero:
    esto significa que "gratis" ya tenemos campos como username, email,
    password (encriptado), first_name, last_name, is_active, is_staff,
    y todo el sistema de autenticación de Django funcionando.

    Acá solo agregamos los campos que son específicos de nuestro negocio
    y que no vienen incluidos por defecto.
    """

    # CharField = campo de texto corto, con un largo máximo obligatorio.
    # blank=True permite que el campo quede vacío en formularios/API.
    province = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Provincia",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ciudad",
    )

    # Para el teléfono usamos texto y no un número entero, porque
    # los teléfonos pueden tener guiones, espacios o el "+" del código
    # de país, y nunca vamos a hacer cuentas matemáticas con ellos.
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono",
    )

    # DateField = solo fecha, sin hora. null=True permite que en la
    # base de datos el valor sea NULL (no todos los usuarios van a
    # cargar su fecha de nacimiento al registrarse).
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de nacimiento",
    )

    # auto_now_add=True: Django completa este campo automáticamente
    # con la fecha/hora exacta en el momento en que se crea el
    # registro, y nunca más se puede modificar desde el código.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    class Meta:
        """
        Clase interna donde Django permite configurar metadatos
        del modelo que no son campos en sí.
        """
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        """
        Define cómo se muestra un objeto User cuando Python lo
        convierte a texto (por ejemplo, en el panel de admin o
        en la consola). Sin esto, Django mostraría algo poco
        útil como "User object (1)".
        """
        return self.get_full_name() or self.username

