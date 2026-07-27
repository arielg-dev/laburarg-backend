from rest_framework import permissions


class IsCompanyMemberOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para Company:

    - Cualquiera (incluso sin loguearse) puede hacer pedidos de
      SOLO LECTURA (GET, HEAD, OPTIONS) -- necesario para que el
      sitio se pueda navegar públicamente.
    - Para pedidos que MODIFICAN datos (POST, PUT, PATCH, DELETE),
      exigimos que el usuario esté autenticado Y sea miembro
      (CompanyMember) de esa empresa puntual.
    """

    def has_permission(self, request, view):
        # Este método se ejecuta ANTES de saber sobre qué objeto
        # puntual se está actuando (por ejemplo, en un POST para
        # crear una empresa nueva, todavía no existe el objeto).
        #
        # SAFE_METHODS es una constante de DRF que agrupa GET, HEAD
        # y OPTIONS -- los métodos que por definición no modifican
        # nada en el servidor.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Para crear una empresa nueva (POST), alcanza con estar
        # logueado -- la validación de "dueño" no aplica todavía
        # porque el objeto no existe hasta que se crea.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Este método SÍ se ejecuta cuando ya existe un objeto
        # puntual de por medio (editar o borrar una Company que
        # ya existe en la base de datos).
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj acá es la instancia de Company sobre la que se quiere
        # actuar. Verificamos que el usuario logueado aparezca
        # entre sus miembros (gracias al related_name="members"
        # que definimos en el modelo CompanyMember).
        return obj.members.filter(user=request.user).exists()

class IsJobCompanyMemberOrReadOnly(permissions.BasePermission):
    """
    Misma lógica que IsCompanyMemberOrReadOnly, pero para Job: acá
    "obj" es un aviso (Job), así que la membresía se chequea contra
    obj.company (la empresa a la que pertenece ese aviso puntual),
    no contra el objeto en sí.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.company.members.filter(user=request.user).exists()