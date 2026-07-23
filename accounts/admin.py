from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Registramos nuestro modelo User personalizado usando UserAdmin
# (la configuración de admin que Django ya trae para el modelo de
# usuario por defecto), para no perder toda la lógica ya armada
# de cómo mostrar contraseñas, permisos, grupos, etc.
admin.site.register(User, UserAdmin)
