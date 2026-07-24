from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Personalización del panel de admin para el modelo Job.

    En vez de admin.site.register(Job) a secas, usamos esta clase
    para controlar exactamente qué columnas mostrar en la lista,
    qué filtros ofrecer en la barra lateral, y por qué campos se
    puede buscar.
    """

    # Columnas que se ven en la lista de resultados (antes solo
    # veíamos el __str__ del modelo en una única columna).
    list_display = (
        "title",
        "company",
        "province",
        "modality",
        "contract_type",
        "status",
        "created_at",
    )

    # Genera filtros clickeables en la barra lateral derecha,
    # uno por cada campo listado acá.
    list_filter = (
        "status",
        "modality",
        "contract_type",
        "province",
    )

    # Habilita la barra de búsqueda arriba de la lista. El doble
    # guión bajo (__) permite buscar en un campo de OTRO modelo
    # relacionado: "company__name" busca por el nombre de la
    # empresa relacionada, no por un campo directo de Job.
    search_fields = (
        "title",
        "company__name",
    )

    # list_editable permite editar el estado directamente desde la
    # lista, sin entrar a cada aviso, muy útil para pausar/cerrar
    # avisos rápido durante pruebas.
    list_editable = ("status",)