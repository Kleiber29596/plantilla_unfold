# apps/gestion/views/autocomplete_select.py
from dal_select2.views                      import Select2QuerySetView
from django.db.models                       import Q
from apps.auxiliares.models.dependencia     import Dependencia, Subdependencia
from apps.auxiliares.models.responsable     import Responsable

class DependenciaAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Dependencia.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs





class SubdependenciaAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Subdependencia.objects.all()

        # Filtro dinámico según dependencia (gracias a forward)
        dependencia_id = self.forwarded.get("dependencia", None)
        if dependencia_id:
            qs = qs.filter(dependencia_id=dependencia_id)
        else:
            qs = Subdependencia.objects.none()

        # Filtro por búsqueda del usuario
        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q))

        return qs

class ResponsableAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Responsable.objects.none()
        subdependencia_id = self.forwarded.get("subdependencia", None)
        if subdependencia_id:
            qs = Responsable.objects.filter(subdependencia_id=subdependencia_id)
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs