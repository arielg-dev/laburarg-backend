"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from companies.views import CompanyViewSet
from jobs.views import JobViewSet
from cvs.views import CVViewSet
from applications.views import ApplicationViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"cvs", CVViewSet, basename="cv")
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"favorites", FavoriteViewSet, basename="favorite")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)