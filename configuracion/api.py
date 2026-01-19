from ninja_extra                            import NinjaExtraAPI
from ninja                                  import NinjaAPI
from apps.cuenta.views.token                import MyTokenObtainPairController, CreateUserController
from ninja.errors                           import ValidationError as NinjaValidationError
from datetime                               import datetime


# Solución robusta al error de recarga:
# Eliminamos todas las ocurrencias del namespace antes de crear la API
NinjaAPI._registry = [n for n in NinjaAPI._registry if n != "demostrador"]

api = NinjaExtraAPI(
                        title           = "Plantilla",
                        description     = "API para Plantillas",
                        urls_namespace  = "demostrador",
                    )



# api.register_controllers(ResetPasswordController)
api.register_controllers(MyTokenObtainPairController)
api.register_controllers(CreateUserController)
