from ninja_extra                            import NinjaExtraAPI
# from django_rest_passwordreset.controller   import ResetPasswordController
from apps.cuenta.views.token                import MyTokenObtainPairController, CreateUserController
from ninja.errors                           import ValidationError as NinjaValidationError
from datetime                               import datetime

from apps.cuenta.views.token                    import router as token_router

api = NinjaExtraAPI(
                        title           = "Plantilla",
                        description     = "API para Plantillas",
                        urls_namespace  = "demostrador",
                    )



api.add_router("/auth/",                token_router)

# api.register_controllers(ResetPasswordController)
api.register_controllers(MyTokenObtainPairController)
api.register_controllers(CreateUserController)


# Manejador de excepciones global para ValidationError
@api.exception_handler(NinjaValidationError)
def validation_error_handler(request, exc):
    
    print('AQUIIIIIIIIIIIIII', exc)
    
    # Extraer el último elemento de cada ubicación (loc), que debería ser el campo problemático
    property = [error["loc"][-1] for error in exc.errors]  # Extrae el último elemento de 'loc'

    # Devolver los campos en la respuesta
    return api.create_response(
        request,
        {
            "statusCode": 400,
            "message": "Error en las propiedades de entrada",
            "property": f"{', '.join(property)}", # Solo devuelve el nombre de los campos problemáticos
            "url": request.path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Añadir fecha y hora actual
        },
        status=400,
    )
    
