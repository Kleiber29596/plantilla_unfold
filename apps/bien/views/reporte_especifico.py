import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from django.http import HttpResponse
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from apps.auxiliares.models.subdependencia import Subdependencia
from django.shortcuts import get_object_or_404, render
from datetime import datetime
import re
from itertools import groupby

# --- Funciones de Estilo ---

def aplicar_formato(celda, font=None, fill=None, alignment=None, width=None):
    """Función para aplicar formato a una celda"""
    if font:
        celda.font = font
    if fill:
        celda.fill = fill
    if alignment:
        celda.alignment = alignment
    if width:
        celda.column_dimension.width = width

def sanitizar_nombre_hoja(nombre):
    """Limpia el nombre para que sea válido como nombre de hoja en Excel"""
    nombre = re.sub(r'[\\/*?:[\]]', '_', nombre)
    if len(nombre) > 31:
        nombre = nombre[:28] + "..."
    return nombre

def crear_hoja_resumen_general(wb, subdependencia, responsables_con_bienes):
    """Crea la hoja de resumen general para la subdependencia"""
    ws_resumen = wb.create_sheet(title="Resumen General")
    
    # Título principal
    ws_resumen.merge_cells('A1:F1')
    titulo = ws_resumen.cell(row=1, column=1)
    titulo.value = f"RESUMEN GENERAL - {subdependencia.nombre.upper()}"
    aplicar_formato(titulo, 
                   Font(size=14, bold=True), 
                   PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"),
                   Alignment(horizontal="center", vertical="center"))
    ws_resumen.row_dimensions[1].height = 30
    
    # Información de la subdependencia
    ws_resumen.cell(row=3, column=1).value = "Subdependencia:"
    ws_resumen.cell(row=3, column=1).font = Font(bold=True)
    ws_resumen.cell(row=3, column=2).value = subdependencia.nombre
    ws_resumen.merge_cells('B3:F3')
    
    ws_resumen.cell(row=4, column=1).value = "Fecha de reporte:"
    ws_resumen.cell(row=4, column=1).font = Font(bold=True)
    ws_resumen.cell(row=4, column=2).value = datetime.now().strftime("%d/%m/%Y %H:%M")
    ws_resumen.merge_cells('B4:F4')
    
    ws_resumen.cell(row=5, column=1).value = "Total de responsables:"
    ws_resumen.cell(row=5, column=1).font = Font(bold=True)
    ws_resumen.cell(row=5, column=2).value = len(responsables_con_bienes)
    ws_resumen.merge_cells('B5:F5')
    
    # Calcular total de bienes
    total_bienes = sum(len(bienes) for _, bienes in responsables_con_bienes)
    ws_resumen.cell(row=6, column=1).value = "Total de bienes asignados:"
    ws_resumen.cell(row=6, column=1).font = Font(bold=True)
    ws_resumen.cell(row=6, column=2).value = total_bienes
    ws_resumen.merge_cells('B6:F6')
    
    # Espacio
    row_num = 8
    
    # Título de la tabla de responsables
    ws_resumen.merge_cells(f'A{row_num}:F{row_num}')
    titulo_tabla = ws_resumen.cell(row=row_num, column=1)
    titulo_tabla.value = "RESPONSABLES Y SUS BIENES ASIGNADOS"
    aplicar_formato(titulo_tabla, 
                   Font(size=12, bold=True), 
                   PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                   Alignment(horizontal="center", vertical="center"))
    row_num += 1
    
    # Encabezados de la tabla
    encabezados = ['No.', 'Nombre del Responsable', 'Cantidad de Bienes', 'Ver Detalle']
    for col_num, encabezado in enumerate(encabezados, 1):
        celda = ws_resumen.cell(row=row_num, column=col_num)
        celda.value = encabezado
        aplicar_formato(celda, 
                       Font(bold=True), 
                       PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
    
    # Ajustar anchos de columnas
    ws_resumen.column_dimensions['A'].width = 8  # No.
    ws_resumen.column_dimensions['B'].width = 40  # Nombre
    ws_resumen.column_dimensions['C'].width = 20  # Cantidad
    ws_resumen.column_dimensions['D'].width = 20  # Ver Detalle
    row_num += 1
    
    # Llenar la tabla con los responsables
    for idx, (responsable, bienes) in enumerate(responsables_con_bienes, 1):
        # Número
        ws_resumen.cell(row=row_num, column=1).value = idx
        ws_resumen.cell(row=row_num, column=1).alignment = Alignment(horizontal="center", vertical="center")
        
        # Nombre del responsable
        ws_resumen.cell(row=row_num, column=2).value = responsable.nombres_apellidos
        ws_resumen.cell(row=row_num, column=2).alignment = Alignment(horizontal="left", vertical="center")
        
        # Cantidad de bienes
        ws_resumen.cell(row=row_num, column=3).value = len(bienes)
        ws_resumen.cell(row=row_num, column=3).alignment = Alignment(horizontal="center", vertical="center")
        
        # Enlace a la hoja del responsable
        nombre_hoja = sanitizar_nombre_hoja(f"R{idx}_{responsable.nombres_apellidos[:20]}")
        celda_enlace = ws_resumen.cell(row=row_num, column=4)
        celda_enlace.value = "Ver Detalle →"
        celda_enlace.hyperlink = f"#{nombre_hoja}!A1"
        celda_enlace.font = Font(color="0563C1", underline="single")
        celda_enlace.alignment = Alignment(horizontal="center", vertical="center")
        
        # Aplicar bordes básicos
        for col in range(1, 5):
            ws_resumen.cell(row=row_num, column=col).border = Border(
                left=Side(style='thin', color="A9A9A9"),
                right=Side(style='thin', color="A9A9A9"),
                top=Side(style='thin', color="A9A9A9"),
                bottom=Side(style='thin', color="A9A9A9")
            )
        
        row_num += 1
    
    # Ajustar alturas de fila
    for row in range(1, row_num + 1):
        ws_resumen.row_dimensions[row].height = 20
    
    return ws_resumen

def crear_hoja_responsable(wb, responsable, bienes, num_responsable, total_responsables):
    """Crea una hoja específica para cada responsable"""
    nombre_hoja = sanitizar_nombre_hoja(f"R{num_responsable}_{responsable.nombres_apellidos[:20]}")
    ws = wb.create_sheet(title=nombre_hoja)
    
    # Título principal
    ws.merge_cells('A1:F1')
    titulo = ws.cell(row=1, column=1)
    titulo.value = f"RESPONSABLE: {responsable.nombres_apellidos.upper()}"
    aplicar_formato(titulo, 
                   Font(size=14, bold=True), 
                   PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"),
                   Alignment(horizontal="center", vertical="center"))
    ws.row_dimensions[1].height = 30
    
    # Información del responsable
    ws.cell(row=3, column=1).value = "Subdependencia:"
    ws.cell(row=3, column=1).font = Font(bold=True)
    ws.cell(row=3, column=2).value = responsable.asignacion.subdependencia.nombre if hasattr(responsable, 'asignacion') and responsable.asignacion and responsable.asignacion.subdependencia else 'N/A'
    ws.merge_cells('B3:F3')
    
    ws.cell(row=4, column=1).value = "Responsable:"
    ws.cell(row=4, column=1).font = Font(bold=True)
    ws.cell(row=4, column=2).value = responsable.nombres_apellidos
    ws.merge_cells('B4:F4')
    
    ws.cell(row=5, column=1).value = "Total de bienes asignados:"
    ws.cell(row=5, column=1).font = Font(bold=True)
    ws.cell(row=5, column=2).value = len(bienes)
    ws.merge_cells('B5:F5')
    
    ws.cell(row=6, column=1).value = "Responsable número:"
    ws.cell(row=6, column=1).font = Font(bold=True)
    ws.cell(row=6, column=2).value = f"{num_responsable} de {total_responsables}"
    ws.merge_cells('B6:F6')
    
    # Enlace de regreso al resumen
    ws.cell(row=8, column=1).value = "← Volver al Resumen General"
    celda_regreso = ws.cell(row=8, column=1)
    celda_regreso.hyperlink = f"#Resumen General!A1"
    celda_regreso.font = Font(color="0563C1", underline="single")
    
    # Espacio
    row_num = 10
    
    # Título de la tabla de bienes
    ws.merge_cells(f'A{row_num}:F{row_num}')
    titulo_tabla = ws.cell(row=row_num, column=1)
    titulo_tabla.value = "BIENES ASIGNADOS"
    aplicar_formato(titulo_tabla, 
                   Font(size=12, bold=True), 
                   PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                   Alignment(horizontal="center", vertical="center"))
    row_num += 1
    
    # Encabezados de la tabla de bienes
    cabeceras = ['Código', 'Tipo', 'Marca', 'Modelo', 'Serial', 'Condición']
    for col_num, cabecera in enumerate(cabeceras, 1):
        celda = ws.cell(row=row_num, column=col_num)
        celda.value = cabecera
        aplicar_formato(celda, 
                       Font(bold=True), 
                       PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
    row_num += 1
    
    # Escribir los bienes del responsable
    for detalle in bienes:
        datos_fila = [
            detalle.bien.codigo_bien if detalle.bien.codigo_bien else 'sin datos',
            detalle.bien.tipo_bien.nombre if detalle.bien.tipo_bien and detalle.bien.tipo_bien.nombre else 'sin datos',
            detalle.bien.marca.nombre if detalle.bien.marca and detalle.bien.marca.nombre else 'sin datos',
            detalle.bien.modelo.nombre if detalle.bien.modelo and detalle.bien.modelo.nombre else 'sin datos',
            detalle.bien.serial if detalle.bien.serial else 'sin datos',
            detalle.bien.condicion.nombre if detalle.bien.condicion and detalle.bien.condicion.nombre else 'sin datos'
        ]
        
        for col_num, dato in enumerate(datos_fila, 1):
            celda = ws.cell(row=row_num, column=col_num)
            celda.value = dato
            
            # Aplicar borde
            celda.border = Border(
                left=Side(style='thin', color="A9A9A9"),
                right=Side(style='thin', color="A9A9A9"),
                top=Side(style='thin', color="A9A9A9"),
                bottom=Side(style='thin', color="A9A9A9")
            )
            
            # Aplicar alineación
            if col_num == 1:  # Código
                celda.alignment = Alignment(horizontal="center", vertical="center")
            else:
                celda.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            
            # Fuente normal
            celda.font = Font(size=10)
        row_num += 1
    
    # Agregar total al final
    if len(bienes) > 0:
        ws.merge_cells(f'A{row_num}:E{row_num}')
        ws.cell(row=row_num, column=1).value = f"TOTAL DE BIENES: {len(bienes)}"
        ws.cell(row=row_num, column=1).font = Font(bold=True, size=11)
        ws.cell(row=row_num, column=1).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row=row_num, column=1).fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")
        
        # Aplicar bordes a la celda de total
        for col in range(1, 7):
            ws.cell(row=row_num, column=col).border = Border(
                left=Side(style='thin', color="A9A9A9"),
                right=Side(style='thin', color="A9A9A9"),
                top=Side(style='thin', color="A9A9A9"),
                bottom=Side(style='thin', color="A9A9A9")
            )
    
    # Ajustar anchos de columna
    anchos_columna = {'A': 25, 'B': 20, 'C': 20, 'D': 20, 'E': 25, 'F': 20}
    for col, ancho in anchos_columna.items():
        ws.column_dimensions[col].width = ancho
    
    # Ajustar altura de filas
    for row in range(1, row_num + 2):
        ws.row_dimensions[row].height = 20
    
    return ws

# --- Vista Principal del Reporte Específico por Subdependencia ---

def vista_seleccion_subdependencia(request):
    """
    Vista para listar subdependencias y permitir descargar su reporte.
    """
    subdependencias = Subdependencia.objects.all().order_by('dependencia__nombre', 'nombre')
    
    context = {
        'subdependencias': subdependencias,
        'titulo': 'Seleccionar Subdependencia para Reporte'
    }
    # Asegúrate de tener un template o usa un HttpResponse simple si no lo tienes
    return render(request, 'bien/reportes/seleccionar_subdependencia.html', context)

def exportar_bienes_por_subdependencia_detallado(request, subdependencia_id):
    """
    Genera un reporte en Excel específico para una subdependencia,
    con una pestaña de Resumen General y luego una pestaña por cada responsable.
    """
    # Obtener la subdependencia específica
    subdependencia = get_object_or_404(Subdependencia, id=subdependencia_id)
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    filename = f"reporte_{subdependencia.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 1. Obtener los datos para la subdependencia específica
    # Usar el campo 'devuelto' en lugar de la relación con detalles_devolucion
    try:
        # Intentar con el filtro devuelto=False
        detalles_asignacion = DetalleAsignacion.objects.filter(
            devuelto=False,
            asignacion__subdependencia=subdependencia
        ).select_related(
            'bien', 'bien__tipo_bien', 'bien__marca', 'bien__modelo',
            'asignacion__usuario', 'asignacion__subdependencia',
            'bien__condicion'
        ).order_by(
            'asignacion__usuario__nombres_apellidos'
        )
    except:
        # Si falla (campo devuelto no existe), obtener todos los registros
        detalles_asignacion = DetalleAsignacion.objects.filter(
            asignacion__subdependencia=subdependencia
        ).select_related(
            'bien', 'bien__tipo_bien', 'bien__marca', 'bien__modelo',
            'asignacion__usuario', 'asignacion__subdependencia',
            'bien__condicion'
        ).order_by(
            'asignacion__usuario__nombres_apellidos'
        )

    wb = openpyxl.Workbook()
    
    # Eliminar la hoja por defecto
    if 'Sheet' in wb.sheetnames:
        ws_default = wb['Sheet']
        wb.remove(ws_default)
    
    # Verificar si hay datos
    if not detalles_asignacion.exists():
        # Crear una hoja con mensaje de que no hay datos
        ws = wb.create_sheet(title="Sin Datos")
        ws.sheet_view.showGridLines = False
        
        # Título principal
        ws['A1'] = f"REPORTE DE BIENES - {subdependencia.nombre.upper()}"
        aplicar_formato(ws['A1'], Font(size=16, bold=True), 
                       PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"), 
                       Alignment(horizontal="center", vertical="center"))
        ws.merge_cells('A1:F1')
        
        # Mensaje principal
        ws['A3'] = f"No hay bienes asignados en {subdependencia.nombre}"
        ws['A3'].alignment = Alignment(horizontal="center", vertical="center")
        ws['A3'].font = Font(size=14)
        ws.merge_cells('A3:F3')
        
        # Información adicional
        ws['A5'] = "Fecha del reporte:"
        ws['A5'].font = Font(bold=True)
        ws['B5'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        ws['A6'] = "Observación:"
        ws['A6'].font = Font(bold=True)
        if 'devuelto' in [f.name for f in DetalleAsignacion._meta.get_fields()]:
            ws['B6'] = "Este reporte muestra únicamente bienes que aún no han sido devueltos"
        else:
            ws['B6'] = "Este reporte muestra todos los bienes asignados en esta subdependencia"
        ws.merge_cells('B6:F6')
        
        # Ajustar anchos
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            ws.column_dimensions[col].width = 20
        
        # Ajustar alturas
        for row in [1, 3, 5, 6]:
            ws.row_dimensions[row].height = 25
        
        wb.active = ws
        wb.save(response)
        return response
    
    # 2. Agrupar por Responsable
    # Convertir a lista y ordenar para groupby
    detalles_lista = list(detalles_asignacion)
    detalles_lista.sort(key=lambda x: x.asignacion.usuario.nombres_apellidos if x.asignacion and x.asignacion.usuario else "")
    
    responsables_con_bienes = []
    
    for responsable, grupo_resp in groupby(detalles_lista, key=lambda x: x.asignacion.usuario if x.asignacion else None):
        if not responsable:
            continue  # Saltar si no hay responsable
        
        bienes_responsable = list(grupo_resp)
        if bienes_responsable:  # Solo agregar si tiene bienes
            responsables_con_bienes.append((responsable, bienes_responsable))
    
    # Si no hay responsables, mostrar mensaje
    if not responsables_con_bienes:
        ws = wb.create_sheet(title="Sin Responsables")
        ws['A1'] = f"REPORTE - {subdependencia.nombre.upper()}"
        aplicar_formato(ws['A1'], Font(size=16, bold=True), 
                       PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"), 
                       Alignment(horizontal="center", vertical="center"))
        ws.merge_cells('A1:F1')
        
        ws['A3'] = f"No hay responsables con bienes asignados en {subdependencia.nombre}"
        ws['A3'].alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells('A3:F3')
        
        wb.active = ws
        wb.save(response)
        return response
    
    # 3. Crear la hoja de Resumen General
    crear_hoja_resumen_general(wb, subdependencia, responsables_con_bienes)
    
    # 4. Crear una hoja por cada responsable
    total_responsables = len(responsables_con_bienes)
    for idx, (responsable, bienes) in enumerate(responsables_con_bienes, 1):
        crear_hoja_responsable(wb, responsable, bienes, idx, total_responsables)
    
    # 5. Mover la hoja de Resumen General al principio
    if "Resumen General" in wb.sheetnames:
        resumen_sheet = wb["Resumen General"]
        wb._sheets.insert(0, wb._sheets.pop(wb._sheets.index(resumen_sheet)))
    
    # 6. Asegurar que la hoja de Resumen General sea la activa
    wb.active = wb["Resumen General"]
    
    wb.save(response)
    return response