from django.contrib import admin

from .models import Application, Favorite


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "status",
        "applied_at",
    )

    list_filter = ("status",)

    search_fields = (
        "user__username",
        "job__title",
    )

    list_editable = ("status",)

    # date_hierarchy agrega una navegación por fechas arriba de la
    # lista (año > mes > día), muy útil cuando haya muchas
    # postulaciones y quieras ver solo las de una fecha puntual.
    date_hierarchy = "applied_at"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "created_at",
    )

    search_fields = (
        "user__username",
        "job__title",
    )