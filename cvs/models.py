from django.conf import settings
from django.db import models


class CV(models.Model):
    """
    Representa un currículum subido por un usuario.

    Un usuario puede subir varios CVs (por ejemplo, uno orientado a
    desarrollo y otro a soporte técnico), y marcar cuál es el que
    usa por defecto al postularse con un clic.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cvs",
        verbose_name="Usuario",
    )

    title = models.CharField(
        max_length=150,
        verbose_name="Título",
        help_text="Ej: 'CV - Desarrollo Backend'",
    )

    # FileField: Django no guarda el archivo DENTRO de la base de
    # datos. Lo guarda físicamente en disco (en desarrollo) o en un
    # servicio como S3 (en producción, cuando lo configuremos), y
    # en esta columna solo se guarda la RUTA hacia ese archivo.
    #
    # upload_to define la subcarpeta donde se van a guardar. El
    # "%Y/%m/" hace que Django organice los archivos automáticamente
    # en subcarpetas por año y mes (ej: cvs/2026/07/archivo.pdf),
    # para no terminar con miles de archivos sueltos en una sola
    # carpeta plana.
    file = models.FileField(
        upload_to="cvs/%Y/%m/",
        verbose_name="Archivo",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="CV principal",
        help_text="El que se usa por defecto al postularse con un clic",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida",
    )

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.title} — {self.user}"