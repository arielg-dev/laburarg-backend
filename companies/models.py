from django.conf import settings
from django.db import models


class Company(models.Model):
    """
    Representa una empresa o consultora que publica búsquedas
    laborales en LaburArg.

    No separamos "empresa" y "consultora" en dos modelos distintos:
    comparten casi todos los campos, así que las diferenciamos con
    el campo booleano `is_agency`. Esto evita duplicar estructura
    y lógica para dos entidades que en el fondo son muy parecidas.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Razón social / Nombre",
    )

    # El CUIT argentino tiene un formato conocido (XX-XXXXXXXX-X),
    # pero lo guardamos como texto y no como número: nunca vamos a
    # hacer cuentas matemáticas con él, y el guión rompería un campo
    # numérico. unique=True evita que se registre la misma empresa
    # dos veces con el mismo CUIT.
    cuit = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="CUIT",
    )

    # Este es el campo clave para diferenciar el modelo de negocio:
    # False = empresa común (5 búsquedas gratis por mes)
    # True  = consultora/agencia de RR.HH. (requiere plan pago)
    is_agency = models.BooleanField(
        default=False,
        verbose_name="Es consultora/agencia",
    )

    # Empresas verificadas manualmente por el equipo de LaburArg,
    # para mostrar un check de confianza (como viste en el aviso
    # de Telemercado: "Empresa verificada").
    verified = models.BooleanField(
        default=False,
        verbose_name="Verificada",
    )

    website = models.URLField(
        blank=True,
        verbose_name="Sitio web",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name


class CompanyMember(models.Model):
    """
    Tabla intermedia que resuelve la relación muchos-a-muchos entre
    User y Company: qué usuarios administran la cuenta de qué
    empresa, y con qué rol.

    Un usuario puede administrar varias empresas (por ejemplo, un
    reclutador de una consultora que maneja varias cuentas cliente),
    y una empresa puede tener varios usuarios administrándola
    (dueño, reclutador, etc.).
    """

    # Roles posibles. Usar `choices` le dice a Django (y a DRF, y al
    # admin) que este campo solo puede tener uno de estos valores
    # específicos, no cualquier texto libre.
    class Role(models.TextChoices):
        OWNER = "owner", "Dueño/a"
        RECRUITER = "recruiter", "Reclutador/a"

    # ForeignKey = relación "muchos a uno". Cada fila de CompanyMember
    # apunta a UN user y a UNA company, pero un mismo user o company
    # puede aparecer en muchas filas de CompanyMember. Sumando las
    # dos ForeignKey, logramos el efecto de "muchos a muchos".
    #
    # settings.AUTH_USER_MODEL en vez de importar User directamente:
    # es la forma recomendada por Django para referenciar el modelo
    # de usuario activo del proyecto, evitando problemas de
    # dependencias circulares entre apps.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships",
        verbose_name="Usuario",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Empresa",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.RECRUITER,
        verbose_name="Rol",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
    )

    class Meta:
        verbose_name = "Miembro de empresa"
        verbose_name_plural = "Miembros de empresa"
        # unique_together evita que el mismo usuario quede
        # registrado dos veces como miembro de la misma empresa.
        unique_together = ("user", "company")

    def __str__(self):
        return f"{self.user} — {self.company} ({self.get_role_display()})"