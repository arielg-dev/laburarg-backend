"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from companies.views import CompanyViewSet
from jobs.views import JobViewSet

# El DefaultRouter de DRF genera automáticamente todas las URLs
# de un ViewSet (list, retrieve, create, update, delete), a partir
# de un solo registro. En vez de escribir 5 líneas de "path(...)"
# por cada modelo, escribimos una sola línea "router.register(...)".
router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"jobs", JobViewSet, basename="job")

urlpatterns = [
    path("admin/", admin.site.urls),
    # include() "engancha" todas las URLs que generó el router bajo
    # el prefijo "api/". Por eso las rutas finales van a quedar
    # como /api/companies/, /api/jobs/, etc.
    path("api/", include(router.urls)),
]

# Solo en desarrollo (DEBUG=True): le decimos a Django que sirva
# los archivos subidos (media/) directamente, para poder ver o
# descargar un CV subido desde el navegador mientras programamos.
# En producción esto lo va a manejar Nginx, no Django directamente.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)