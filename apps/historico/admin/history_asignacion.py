# tienda/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin # Importa SimpleHistoryAdmin
from apps.historico.models.history_asignacion import HistoricoAsignacion

@admin.register(HistoricoAsignacion)
class HistoryAsignacionAdmin(SimpleHistoryAdmin): # Hereda de SimpleHistoryAdmin
    list_display = ('bien', 'responsable', 'subdependencia','estatus','motivo', 'history_type','history_date')

    # Puedes añadir tus propias configuraciones de admin aquí