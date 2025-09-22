from ninja_extra                            import NinjaExtraAPI
from apps.cuenta.views.token                import MyTokenObtainPairController, CreateUserController
from ninja.errors                           import ValidationError as NinjaValidationError
from datetime                               import datetime
from apps.cuenta.views.token                import router as token_router
from configuracion.core.api_servicio        import router as api_servicio
from apps.gestion.views.bien                import router as bienes_router
from apps.auxiliares.views.categoria        import router as categoria_router
from apps.auxiliares.views.modelo           import router as modelo_router    
from apps.gestion.views.prestamos           import router as prestamos_router
from apps.auxiliares.views.auxiliares       import router as auxiliares_router

api = NinjaExtraAPI(
                        title           = "Plantilla",
                        description     = "API para Plantillas",
                        urls_namespace  = "demostrador",
                    )



api.add_router("/auth/",      token_router)
api.add_router("/servicio/",  api_servicio)  # Puedes cambiar la ruta base si deseas
api.add_router("/bienes/",    bienes_router) 
api.add_router("/categoria/", categoria_router)
api.add_router("/modelo/",    modelo_router)
api.add_router("/prestamos/", prestamos_router)
api.add_router("/auxiliares/",auxiliares_router)

# api.register_controllers(ResetPasswordController)
api.register_controllers(MyTokenObtainPairController)
api.register_controllers(CreateUserController)
