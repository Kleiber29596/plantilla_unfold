from ninja_extra                            import NinjaExtraAPI
from apps.cuenta.views.token                import MyTokenObtainPairController, CreateUserController
from ninja.errors                           import ValidationError as NinjaValidationError
from datetime                               import datetime
from apps.cuenta.views.token                import router as token_router



api = NinjaExtraAPI(
                        title           = "Plantilla",
                        description     = "API para Plantillas",
                        urls_namespace  = "demostrador",
                    )



# api.register_controllers(ResetPasswordController)
api.register_controllers(MyTokenObtainPairController)
api.register_controllers(CreateUserController)
