from django.conf import settings
from django.db import models

from cvs.models import CV
from jobs.models import Job


class Application(models.Model):
    """
    Representa la postulación de un usuario a una búsqueda laboral,
    usando un CV específico.

    Es el modelo con más relaciones del sistema: conecta User, Job
    y CV al mismo tiempo. Por eso tiene tres ForeignKey distintas.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        VIEWED = "viewed", "Vista"
        REJECTED = "rejected", "Rechazada"
        ACCEPTED = "accepted", "Aceptada"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Usuario",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Búsqueda laboral",
    )

    # PROTECT en vez de CASCADE: si alguien intenta borrar un CV que
    # ya fue usado en una postulación, Django va a IMPEDIR el borrado
    # en vez de borrar la postulación en cadena. Tiene sentido: una
    # postulación ya enviada es un registro histórico importante
    # (para la empresa, y como evidencia para el propio usuario) y
    # no debería desaparecer solo porque alguien borró un archivo.
    cv = models.ForeignKey(
        CV,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="CV utilizado",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )

    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de postulación",
    )

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ["-applied_at"]
        # Evita que el mismo usuario se postule dos veces al mismo
        # aviso. Es una regla de negocio real, no solo prolijidad
        # de datos: no tendría sentido postularse repetidamente.
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user} → {self.job} ({self.get_status_display()})"


class Favorite(models.Model):
    """
    Un aviso que un usuario guardó como favorito para verlo después,
    sin haberse postulado todavía.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Usuario",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Búsqueda laboral",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de guardado",
    )

    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        ordering = ["-created_at"]
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user} ♥ {self.job}"