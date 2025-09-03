from django import forms
from apps.gestion.models.asignacion import Asignacion


class AsignacionForm(forms.ModelForm):
    """Formulario para crear / editar asignaciones.

    - Añade un ``onchange`` al ``<select>`` de *estatus* para disparar
      la función ``toggleMotivoField`` definida en ``js/deshabilitar_asignacion.js``.
    - Carga automáticamente ese script mediante la clase interna ``Media``.
    """

    class Meta:
        model = Asignacion
        fields = [
            "bien",
            "responsable",
            "dependencia",
            "subdependencia"
            "fecha_asignacion",
            "estatus",
            "motivo",
        ]

        # Widgets personalizados
        widgets = {
            "fecha_asignacion": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "vDateField",  # clase por defecto del admin
                }
            ),
            "estatus": forms.Select(
                attrs={
                    "id": "id_estatus",  # asegúrate de que coincide con el selector JS
                    "class": "vSelect",   # clase por defecto del admin
                    "onchange": "toggleMotivoField();",  # dispara la función JS
                }
            ),
            "motivo": forms.Textarea(
                attrs={
                    "rows": 3,
                    "cols": 40,
                }
            ),
        }

        labels = {
            "bien": "Bien",
            "responsable": "Responsable",
            "dependencia": "Dependencia",
            "subdependencia": "Subdependencia",
            "fecha_asignacion": "Fecha de asignación",
            "estatus": "Estatus",
            "motivo": "Motivo",
        }

    class Media:
        # Django incluirá este script al renderizar el formulario en el admin
        js = (
            "js/deshabilitar_asignacion.js",  # ruta relativa en tu carpeta STATICFILES
        )
