from django.contrib  import admin
from django.urls     import path, include
from apps.auxiliares import views

from apps.frontend.views                    import inicio
from .api                                   import api
from apps.cuenta.views.consultar_cargo      import consultar_cargo
from apps.gestion.views.autocomplete_select import DependenciaAutocomplete, SubdependenciaAutocomplete, ResponsableAutocomplete

urlpatterns =   [
                    path('',            inicio,             name = 'inicio'             ),
                    path("admin/",      admin.site.urls),
                    path('consultar-cargo/', consultar_cargo, name='consultar_cargo'),
                    path('', include('apps.gestion.urls')),
                    path("", api.urls),
                    path("dependencia-autocomplete/", DependenciaAutocomplete.as_view(), name="dependencia-autocomplete"),
                    path("subdependencia-autocomplete/", SubdependenciaAutocomplete.as_view(), name="subdependencia-autocomplete"),
                    path("responsable-autocomplete/", ResponsableAutocomplete.as_view(), name="responsable-autocomplete"),

                         
                                                                    

                ]
