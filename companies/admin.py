from django.contrib import admin

from .models import Company, CompanyMember


class CompanyMemberInline(admin.TabularInline):
    """
    Un "inline" muestra un modelo relacionado directamente dentro
    de la página de edición de otro modelo, en vez de tener que ir
    a buscarlo por separado en su propia sección.

    Acá: al editar una Company, vamos a ver debajo la lista de sus
    CompanyMember (quiénes la administran) directamente en la misma
    pantalla, con la posibilidad de agregar/quitar sin salir de ahí.
    """
    model = CompanyMember
    extra = 1  # cuántas filas vacías extra mostrar para cargar rápido


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cuit",
        "is_agency",
        "verified",
        "created_at",
    )

    list_filter = (
        "is_agency",
        "verified",
    )

    search_fields = (
        "name",
        "cuit",
    )

    # Acá "enchufamos" el inline que definimos arriba.
    inlines = [CompanyMemberInline]


@admin.register(CompanyMember)
class CompanyMemberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "role",
        "created_at",
    )

    list_filter = ("role",)

    search_fields = (
        "user__username",
        "company__name",
    )