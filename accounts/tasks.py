from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_welcome_email(user_id):
    """
    Envía un email de bienvenida a un usuario recién registrado.

    @shared_task: el decorador que convierte esta función común de
    Python en una tarea que Celery puede ejecutar en segundo plano.
    "shared" significa que no depende de una instancia específica
    de la app Celery -- útil para tareas definidas dentro de una
    app de Django, como esta.

    Recibimos "user_id" (un número) en vez del objeto User
    completo a propósito: Celery serializa los argumentos de la
    tarea a JSON para mandarlos a través de Redis, y un objeto
    complejo de Django no se puede convertir a JSON fácilmente.
    Pasar solo el ID, y volver a buscar el usuario DENTRO de la
    tarea, es el patrón estándar.
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(id=user_id)

    send_mail(
        subject="¡Bienvenido/a a LaburArg!",
        message=(
            f"Hola {user.first_name or user.username},\n\n"
            "Gracias por registrarte en LaburArg. Ya podés completar "
            "tu perfil, subir tu CV y empezar a postularte a las "
            "búsquedas laborales que más te interesen.\n\n"
            "¡Éxitos en tu búsqueda!"
        ),
        from_email="no-reply@laburarg.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    return f"Email de bienvenida enviado a {user.email}"