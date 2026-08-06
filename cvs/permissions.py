from rest_framework import permissions


class HasCVDatabaseAccess(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios logueados que sean miembros
    de AL MENOS una empresa con una suscripción activa que otorgue
    acceso a la base de CVs (planes pagos).
    """

    message = (
        "Necesitás una suscripción activa (plan Profesional o "
        "Agencia) para buscar en la base de CVs."
    )

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Recorremos todas las empresas de las que el usuario es
        # miembro (company_memberships, gracias al related_name
        # que definimos en CompanyMember), y alcanza con que UNA
        # sola tenga acceso habilitado.
        for membership in request.user.company_memberships.all():
            subscription = getattr(membership.company, "subscription", None)
            if subscription and subscription.has_cv_database_access:
                return True

        return False