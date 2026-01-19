import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from itertools import groupby
from datetime import datetime
import re

# --- Funciones de Estilo Mejoradas basadas en el reporte de formación ---

def aplicar_formato(celda, font=None, fill=None, alignment=None, width=None):
    """Función para aplicar formato a una celda, copiada del reporte de formación"""
    if font:
        celda.font = font
    if fill:
        celda.fill = fill
    if alignment:
        celda.alignment = alignment
    if width:
        celda.column_dimension.width = width

def get_estilos():
    """Retorna un diccionario con todos los estilos visuales mejorados"""
    
    # Colores del reporte de formación
    COLOR_PRIMARIO = "B7B7B7"  # Gris para encabezados (igual que en formación)
    COLOR_SECUNDARIO = "D9D9D9"  # Gris más claro (igual que en formación)
    COLOR_TEXTO_OSCURO = "000000"
    COLOR_BORDE = "A9A9A9"
    COLOR_ENCABEZADO_TABLA = "C0C0C0"
    
    # Definir bordes como en el reporte de formación
    borde_delgado = Border(
        left=Side(style='thin', color=COLOR_BORDE),
        right=Side(style='thin', color=COLOR_BORDE),
        top=Side(style='thin', color=COLOR_BORDE),
        bottom=Side(style='thin', color=COLOR_BORDE)
    )
    
    # Fuentes como en el reporte de formación
    bold_font = Font(bold=True)
    font_titulo = Font(size=14, bold=True)
    font_subtitulo = Font(size=12, bold=True)
    font_normal = Font(size=10)
    
    # Alineaciones como en el reporte de formación
    center_alignment = Alignment(horizontal="center", vertical="center")
    left_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    
    # Rellenos como en el reporte de formación
    header_fill = PatternFill(start_color=COLOR_PRIMARIO, end_color=COLOR_PRIMARIO, fill_type="solid")
    subheader_fill = PatternFill(start_color=COLOR_SECUNDARIO, end_color=COLOR_SECUNDARIO, fill_type="solid")
    table_header_fill = PatternFill(start_color=COLOR_ENCABEZADO_TABLA, end_color=COLOR_ENCABEZADO_TABLA, fill_type="solid")
    
    return {
        'titulo': {
            'font': font_titulo,
            'fill': header_fill,
            'alignment': center_alignment,
            'border': borde_delgado
        },
        'subtitulo': {
            'font': font_subtitulo,
            'fill': subheader_fill,
            'alignment': center_alignment,
            'border': borde_delgado
        },
        'encabezado_tabla': {
            'font': bold_font,
            'fill': table_header_fill,
            'alignment': center_alignment,
            'border': borde_delgado
        },
        'dato': {
            'font': font_normal,
            'alignment': left_alignment,
            'border': borde_delgado
        },
        'dato_centrado': {
            'font': font_normal,
            'alignment': center_alignment,
            'border': borde_delgado
        },
        'total': {
            'font': Font(bold=True, size=10),
            'alignment': center_alignment,
            'border': borde_delgado
        }
    }

def aplicar_estilo_rango(hoja, rango, estilo):
    """Aplica estilos a un rango de celdas, idealmente fusionadas"""
    min_col, min_row, max_col, max_row = openpyxl.utils.range_boundaries(rango)
    
    for row in hoja.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for celda in row:
            if 'font' in estilo: celda.font = estilo['font']
            if 'fill' in estilo: celda.fill = estilo['fill']
            if 'alignment' in estilo: celda.alignment = estilo['alignment']
            if 'border' in estilo: celda.border = estilo['border']

def ajustar_ancho_columnas(hoja, anchos):
    """Ajusta el ancho de las columnas según un diccionario"""
    for col_letra, ancho in anchos.items():
        hoja.column_dimensions[col_letra].width = ancho

def sanitizar_nombre_hoja(nombre):
    """Limpia el nombre para que sea válido como nombre de hoja en Excel"""
    # Reemplazar caracteres inválidos
    nombre = re.sub(r'[\\/*?:[\]]', '_', nombre)
    # Limitar longitud a 31 caracteres (límite de Excel)
    if len(nombre) > 31:
        nombre = nombre[:28] + "..."
    return nombre

# --- Vista Principal del Reporte ---

def exportar_bienes_por_responsable_excel(request):
    """
    Genera un reporte en Excel de bienes asignados, agrupados por 
    Subdependencia y luego por Responsable, con una pestaña por cada subdependencia.
    """
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="reporte_bienes_{datetime.now().strftime("%Y%m%d")}.xlsx"'

    # OPCIÓN 1: Filtro simple usando el campo 'devuelto' que mencionaste anteriormente
    # Según un error anterior que mostraste, el campo 'devuelto' existe en DetalleAsignacion
    try:
        detalles_asignacion = DetalleAsignacion.objects.filter(
            devuelto=False  # Solo bienes que no han sido devueltos
        ).select_related(
            'bien', 'bien__tipo_bien', 'bien__marca', 'bien__modelo',
            'asignacion__usuario', 'asignacion__subdependencia',
            'bien__condicion'
        ).order_by(
            'asignacion__subdependencia__nombre', 
            'asignacion__usuario__nombres_apellidos'
        )
    except Exception as e:
        # Si falla, intentamos otra opción
        print(f"Error con devuelto=False: {e}")
        
        # OPCIÓN 2: Mostrar todos los bienes sin filtrar
        detalles_asignacion = DetalleAsignacion.objects.select_related(
            'bien', 'bien__tipo_bien', 'bien__marca', 'bien__modelo',
            'asignacion__usuario', 'asignacion__subdependencia',
            'bien__condicion'
        ).order_by(
            'asignacion__subdependencia__nombre', 
            'asignacion__usuario__nombres_apellidos'
        ).all()

    wb = openpyxl.Workbook()
    
    # Eliminar la hoja por defecto que crea openpyxl si existe
    if 'Sheet' in wb.sheetnames:
        ws_default = wb['Sheet']
        wb.remove(ws_default)
    
    estilos = get_estilos()
    
    # Verificar si hay datos
    if not detalles_asignacion.exists():
        # Crear una hoja con mensaje de que no hay datos
        ws = wb.create_sheet(title="Sin Datos")
        ws.sheet_view.showGridLines = False
        
        # Título principal
        ws['A1'] = "REPORTE DE BIENES POR RESPONSABLE"
        aplicar_formato(ws['A1'], Font(size=16, bold=True), 
                       PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"), 
                       Alignment(horizontal="center", vertical="center"))
        ws.merge_cells('A1:F1')
        
        # Mensaje principal
        ws['A3'] = "No hay bienes asignados"
        aplicar_formato(ws['A3'], Font(size=14), None, Alignment(horizontal="center", vertical="center"))
        ws.merge_cells('A3:F3')
        
        # Información adicional
        ws['A5'] = "Fecha del reporte:"
        aplicar_formato(ws['A5'], Font(bold=True), None, None)
        
        ws['B5'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        aplicar_formato(ws['B5'], None, None, None)
        
        ws['A6'] = "Observación:"
        aplicar_formato(ws['A6'], Font(bold=True), None, None)
        
        ws['B6'] = "Este reporte muestra todos los bienes asignados"
        aplicar_formato(ws['B6'], None, None, None)
        
        # Ajustar anchos
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            ws.column_dimensions[col].width = 20
        
        # Ajustar alturas
        for row in [1, 3, 5, 6]:
            ws.row_dimensions[row].height = 25
        
        # Asegurar que haya al menos una hoja visible y activa
        wb.active = ws
        
        wb.save(response)
        return response
    
    # Diccionario para agrupar todos los datos por subdependencia
    datos_por_subdependencia = {}
    
    # 2. Agrupar por Subdependencia (nivel superior)
    key_subdependencia = lambda x: x.asignacion.subdependencia
    for subdependencia, grupo_subdep in groupby(detalles_asignacion, key=key_subdependencia):
        grupo_subdep_lista = list(grupo_subdep)
        
        # Almacenar los datos de esta subdependencia
        datos_por_subdependencia[subdependencia] = {
            'grupo_subdep_lista': grupo_subdep_lista,
            'responsables': {}
        }
        
        # 3. Agrupar por Responsable dentro de esta subdependencia
        key_responsable = lambda x: x.asignacion.usuario
        for responsable, grupo_resp in groupby(grupo_subdep_lista, key=key_responsable):
            datos_por_subdependencia[subdependencia]['responsables'][responsable] = list(grupo_resp)
    
    # 4. Crear una hoja por cada subdependencia
    for subdependencia, datos in datos_por_subdependencia.items():
        # Crear nombre válido para la hoja
        nombre_hoja = sanitizar_nombre_hoja(subdependencia.nombre)
        
        # Crear nueva hoja
        ws = wb.create_sheet(title=nombre_hoja)
        row_num = 1
        
        # Título de Subdependencia (estilo igual al reporte de formación)
        ws.merge_cells(f'A{row_num}:F{row_num}')
        ws.cell(row=row_num, column=1).value = f"REPORTE DE BIENES - {subdependencia.nombre.upper()}"
        aplicar_formato(ws.cell(row=row_num, column=1), 
                       Font(size=14, bold=True), 
                       PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
        ws.row_dimensions[row_num].height = 25
        row_num += 2  # Espacio después del título (igual que en formación)
        
        # 5. Agrupar por Responsable (nivel anidado)
        for responsable, grupo_resp in datos['responsables'].items():
            
            # Subtítulo del Responsable (estilo igual al reporte de formación)
            ws.merge_cells(f'A{row_num}:F{row_num}')
            ws.cell(row=row_num, column=1).value = f"Responsable: {responsable.nombres_apellidos}"
            aplicar_formato(ws.cell(row=row_num, column=1), 
                           Font(size=12, bold=True), 
                           PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
                           Alignment(horizontal="center", vertical="center"))
            row_num += 1

            # Encabezados de la tabla de bienes (estilo igual al reporte de formación)
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
            for detalle in grupo_resp:
                datos_fila_original = [
                    detalle.bien.codigo_bien,
                    detalle.bien.tipo_bien.nombre if detalle.bien.tipo_bien else None,
                    detalle.bien.marca.nombre if detalle.bien.marca else None,
                    detalle.bien.modelo.nombre if detalle.bien.modelo else None,
                    detalle.bien.serial,
                    detalle.bien.condicion.nombre if detalle.bien.condicion else None
                ]
                datos_fila = [str(d) if d not in [None, ''] else 'sin datos' for d in datos_fila_original]
                
                for col_num, dato in enumerate(datos_fila, 1):
                    celda = ws.cell(row=row_num, column=col_num)
                    celda.value = dato
                    
                    # Aplicar borde a todas las celdas de datos
                    celda.border = Border(
                        left=Side(style='thin', color="A9A9A9"),
                        right=Side(style='thin', color="A9A9A9"),
                        top=Side(style='thin', color="A9A9A9"),
                        bottom=Side(style='thin', color="A9A9A9")
                    )
                    
                    # Aplicar alineación izquierda para texto, centro para códigos
                    if col_num == 1:  # Código
                        celda.alignment = Alignment(horizontal="center", vertical="center")
                    else:
                        celda.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                    
                    # Fuente normal
                    celda.font = Font(size=10)
                row_num += 1
            
            # Espacio después de cada responsable (2 filas como en formación)
            row_num += 2
        
        # 6. Ajustar anchos de columna para esta hoja
        anchos_columna = {'A': 25, 'B': 20, 'C': 20, 'D': 20, 'E': 25, 'F': 20}
        for col, ancho in anchos_columna.items():
            ws.column_dimensions[col].width = ancho
        
        # Ajustar altura de filas
        for row in range(1, row_num + 1):
            ws.row_dimensions[row].height = 20

    # 7. Crear una hoja de índice/resumen si hay más de una subdependencia
    if len(datos_por_subdependencia) > 1:
        ws_indice = wb.create_sheet(title="Índice")
        ws_indice.sheet_view.showGridLines = False
        
        # Título del índice (estilo igual al reporte de formación)
        ws_indice['A1'] = "ÍNDICE DE SUBDEPENDENCIAS"
        aplicar_formato(ws_indice['A1'], 
                       Font(size=16, bold=True), 
                       PatternFill(start_color="B7B7B7", end_color="B7B7B7", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
        ws_indice.merge_cells('A1:C1')
        ws_indice.row_dimensions[1].height = 25
        
        row_indice = 3
        
        # Encabezados del índice (estilo igual al reporte de formación)
        ws_indice.cell(row=row_indice, column=1).value = "No."
        aplicar_formato(ws_indice.cell(row=row_indice, column=1), 
                       Font(bold=True), 
                       PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
        
        ws_indice.cell(row=row_indice, column=2).value = "Subdependencia"
        aplicar_formato(ws_indice.cell(row=row_indice, column=2), 
                       Font(bold=True), 
                       PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
        
        ws_indice.cell(row=row_indice, column=3).value = "Total Responsables"
        aplicar_formato(ws_indice.cell(row=row_indice, column=3), 
                       Font(bold=True), 
                       PatternFill(start_color="C0C0C0", end_color="C0C0C0", fill_type="solid"),
                       Alignment(horizontal="center", vertical="center"))
        
        row_indice += 1
        
        # Listar todas las subdependencias con hipervínculos
        for idx, (subdependencia, datos) in enumerate(datos_por_subdependencia.items(), 1):
            nombre_hoja = sanitizar_nombre_hoja(subdependencia.nombre)
            
            # Número
            ws_indice.cell(row=row_indice, column=1).value = idx
            ws_indice.cell(row=row_indice, column=1).alignment = Alignment(horizontal="center", vertical="center")
            
            # Nombre con hipervínculo (estilo de enlace)
            celda_nombre = ws_indice.cell(row=row_indice, column=2)
            celda_nombre.value = subdependencia.nombre
            celda_nombre.hyperlink = f"#{nombre_hoja}!A1"
            celda_nombre.font = Font(name='Calibri', size=11, color="0563C1", underline="single")
            celda_nombre.alignment = Alignment(horizontal="left", vertical="center")
            
            # Total de responsables
            ws_indice.cell(row=row_indice, column=3).value = len(datos['responsables'])
            ws_indice.cell(row=row_indice, column=3).alignment = Alignment(horizontal="center", vertical="center")
            
            # Aplicar bordes a la fila
            for col in range(1, 4):
                ws_indice.cell(row=row_indice, column=col).border = Border(
                    left=Side(style='thin', color="A9A9A9"),
                    right=Side(style='thin', color="A9A9A9"),
                    top=Side(style='thin', color="A9A9A9"),
                    bottom=Side(style='thin', color="A9A9A9")
                )
            
            row_indice += 1
        
        # Ajustar anchos de columna del índice
        ws_indice.column_dimensions['A'].width = 8
        ws_indice.column_dimensions['B'].width = 50
        ws_indice.column_dimensions['C'].width = 20
        
        # Ajustar altura de filas del índice
        for row in range(1, row_indice + 1):
            ws_indice.row_dimensions[row].height = 20
        
        # Mover la hoja índice al principio
        indice_sheet = wb["Índice"]
        wb._sheets.insert(0, wb._sheets.pop(wb._sheets.index(indice_sheet)))
    
    # 8. Si solo hay una subdependencia, moverla al principio
    elif len(datos_por_subdependencia) == 1:
        subdependencia = list(datos_por_subdependencia.keys())[0]
        nombre_hoja = sanitizar_nombre_hoja(subdependencia.nombre)
        
        # Asegurarnos de que la hoja existe antes de moverla
        if nombre_hoja in wb.sheetnames:
            ws_unica = wb[nombre_hoja]
            wb._sheets.insert(0, wb._sheets.pop(wb._sheets.index(ws_unica)))
    
    # 9. Asegurar que haya al menos una hoja visible y activa
    if len(wb.sheetnames) == 0:
        # Crear una hoja por defecto si por alguna razón no hay hojas
        ws = wb.create_sheet(title="Reporte")
        ws['A1'] = "Reporte Generado"
        aplicar_formato(ws['A1'], Font(size=14, bold=True), None, Alignment(horizontal="center", vertical="center"))
        ws.merge_cells('A1:F1')
    
    # Establecer la primera hoja como activa
    wb.active = wb.worksheets[0]
    
    wb.save(response)
    return response