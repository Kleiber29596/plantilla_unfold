from django.contrib  import admin
from django.urls     import path, include
from apps.auxiliares import views

from apps.frontend.views                import inicio

from .api                               import api
from apps.cuenta.views.consultar_cargo  import consultar_cargo

urlpatterns =   [
                    path('',            inicio,             name = 'inicio'             ),
                    path("admin/",      admin.site.urls),
                    path('consultar-cargo/', consultar_cargo, name='consultar_cargo'),
                    path('', include('apps.gestion.urls')),
                    path("", api.urls),

                                                                                            

                    


                ]
