from django.contrib  import admin
from django.urls     import path, include
from apps.auxiliares import views

from apps.frontend.views                    import inicio
from .api                                   import api
from apps.cuenta.views.consultar_cargo      import consultar_cargo
from apps.auxiliares.views.autocomplete     import DependenciaAutocomplete, SubdependenciaAutocomplete, MarcaAutocomplete, ModeloAutocomplete
urlpatterns =   [
                    path('',            inicio,             name = 'inicio'             ),
                    path("admin/",      admin.site.urls),
                    path('consultar-cargo/', consultar_cargo, name='consultar_cargo'),
                    path("api", api.urls),
                    path("dependencia-autocomplete/", DependenciaAutocomplete.as_view(), name="dependencia-autocomplete"),
                    path("subdependencia-autocomplete/", SubdependenciaAutocomplete.as_view(), name="subdependencia-autocomplete"),
                    path("marca-autocomplete/", MarcaAutocomplete.as_view(), name="marca-autocomplete"),
                    path("modelo-autocomplete/", ModeloAutocomplete.as_view(), name="modelo-autocomplete"),
                    path('bienes/', include('apps.bien.urls')),
                ]
