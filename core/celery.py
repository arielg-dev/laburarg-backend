import os

from celery import Celery

# Le dice a Celery dónde encontrar la configuración de Django
# (settings.py) antes de arrancar.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# "core" acá es el nombre interno que Celery usa para este proyecto
# de tareas -- no tiene que coincidir con nada más, es solo un
# identificador.
app = Celery("core")

# namespace="CELERY": le dice a Celery que busque, dentro de
# settings.py, todas las variables que empiecen con el prefijo
# CELERY_ (por ejemplo CELERY_BROKER_URL) como su configuración.
# Evita mezclar la config de Celery con el resto de Django.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Busca automáticamente un archivo "tasks.py" dentro de CADA app
# que esté en INSTALLED_APPS, y registra las tareas que encuentre
# ahí. Así no hay que registrar cada tarea a mano una por una.
app.autodiscover_tasks()

