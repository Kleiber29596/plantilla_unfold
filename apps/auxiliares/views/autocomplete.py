from dal import autocomplete
from apps.auxiliares.models.catalogo_bienes import Marca, Modelo
from apps.auxiliares.models.dependencia     import Dependencia 
from apps.auxiliares.models.subdependencia  import Subdependencia

class MarcaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Asegura que solo usuarios autenticados puedan usar el autocompletado
        if not self.request.user.is_authenticated:
            return Marca.objects.none()

        qs = Marca.objects.all()

        # Filtra el queryset si se proporciona un término de búsqueda (self.q)
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs

class ModeloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Modelo.objects.none()

        # 'marca' es el nombre del campo que estamos "reenviando" desde el formulario
        marca_id = self.forwarded.get('marca', None)
        qs = Modelo.objects.all()

        # Filtra los modelos por la marca seleccionada
        if marca_id:
            qs = qs.filter(marca_id=marca_id)

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs

class DependenciaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Dependencia.objects.none()
        qs = Dependencia.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

class SubdependenciaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Subdependencia.objects.none()

        # 'dependencia' es el nombre del campo que estamos "reenviando"
        dependencia_id = self.forwarded.get('dependencia', None)
        qs = Subdependencia.objects.all()

        # Filtra las subdependencias por la dependencia seleccionada
        if dependencia_id:
            qs = qs.filter(dependencia_id=dependencia_id)

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs
