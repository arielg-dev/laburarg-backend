from django.db import models

from companies.models import Company


class Job(models.Model):
    """
    Representa una búsqueda laboral publicada por una empresa.

    Cada Job pertenece a una única Company (relación 1:N: una
    empresa puede publicar muchos avisos, pero cada aviso es de
    una sola empresa).
    """

    class Modality(models.TextChoices):
        ON_SITE = "on_site", "Presencial"
        REMOTE = "remote", "Remoto"
        HYBRID = "hybrid", "Híbrido"

    class ContractType(models.TextChoices):
        PERMANENT = "permanent", "Tiempo indeterminado"
        FIXED_TERM = "fixed_term", "Plazo fijo"
        TEMPORARY = "temporary", "Temporal/Changas"
        INTERNSHIP = "internship", "Pasantía"

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        ACTIVE = "active", "Activa"
        PAUSED = "paused", "Pausada"
        CLOSED = "closed", "Cerrada"

    # related_name="jobs" nos permite escribir despues
    # empresa.jobs.all() para traer todos los avisos de una empresa.
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
        verbose_name="Empresa",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Título del puesto",
    )

    description = models.TextField(
        verbose_name="Descripción",
    )

    # Requisitos como texto libre por ahora. Más adelante, cuando
    # lleguemos a la IA de matching, vamos a poder analizar este
    # texto para compararlo contra el contenido del CV.
    requirements = models.TextField(
        blank=True,
        verbose_name="Requisitos",
    )

    province = models.CharField(
        max_length=100,
        verbose_name="Provincia",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ciudad",
    )

    modality = models.CharField(
        max_length=20,
        choices=Modality.choices,
        default=Modality.ON_SITE,
        verbose_name="Modalidad",
    )

    contract_type = models.CharField(
        max_length=20,
        choices=ContractType.choices,
        default=ContractType.PERMANENT,
        verbose_name="Tipo de contrato",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Estado",
    )

    # Campos de fecha automáticos: created_at se fija una sola vez
    # al crear el registro (auto_now_add), updated_at se actualiza
    # cada vez que se guarda el registro (auto_now). Esta diferencia
    # es clave: usar el que no corresponde es un error común.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de publicación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Búsqueda laboral"
        verbose_name_plural = "Búsquedas laborales"
        # Ordena los resultados por defecto: los avisos más nuevos
        # primero, sin que cada consulta tenga que pedirlo explícitamente.
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.company}"