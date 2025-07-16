# tienda/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin # Importa SimpleHistoryAdmin
from apps.gestion.models.history_asignacion import HistoricoAsignacion

@admin.register(HistoricoAsignacion)
class HistoryAsignacionAdmin(SimpleHistoryAdmin): # Hereda de SimpleHistoryAdmin
    list_display = ('bien', 'responsable', 'ubicacion','fecha_asignacion','estatus','motivo', 'history_type')

    # Puedes añadir tus propias configuraciones de admin aquí