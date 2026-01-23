import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from apps.bien.models.detalle_asignacion import DetalleAsignacion
from itertools import groupby
from datetime import datetime
import re

# --- Funciones de Estilo Mejoradas basadas en el reporte anterior ---

def get_estilos():
    """Retorna un diccionario con todos los estilos visuales mejorados"""
    
    # Paleta de colores profesional - Igual que en el reporte anterior
    COLOR_PRIMARIO = "B7B7B7"  # Gris para todos los títulos
    COLOR_SECUNDARIO = "B7B7B7"  # Gris para encabezados de sección
    COLOR_FONDO_CLARO = "F8FAFC"  # Azul muy claro para filas alternas
    COLOR_TEXTO_BLANCO = "FFFFFF"
    COLOR_TEXTO_OSCURO = "1F2937"
    COLOR_BORDE = "CBD5E1"  # Gris claro para bordes
    COLOR_ENCABEZADO = "B7B7B7"  # Gris para encabezados de tabla
    COLOR_ENCABEZADO_SECCION = "D9D9D9"  # Gris más claro para secciones
    
    # Bordes - Igual que en el reporte anterior
    borde_delgado = Border(
        left=Side(style='thin', color=COLOR_BORDE),
        right=Side(style='thin', color=COLOR_BORDE),
        top=Side(style='thin', color=COLOR_BORDE),
        bottom=Side(style='thin', color=COLOR_BORDE)
    )
    
    borde_grueso = Border(
        left=Side(style='medium', color=COLOR_PRIMARIO),
        right=Side(style='medium', color=COLOR_PRIMARIO),
        top=Side(style='medium', color=COLOR_PRIMARIO),
        bottom=Side(style='medium', color=COLOR_PRIMARIO)
    )
    
    return {
        # Título principal
        'titulo_principal': {
            'font': Font(name='Calibri', size=16, bold=True, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_PRIMARIO, end_color=COLOR_PRIMARIO, fill_type="solid"),
            'alignment': Alignment(horizontal="center", vertical="center", wrap_text=True),
            'border': borde_grueso
        },
        # Encabezados de sección
        'titulo_seccion': {
            'font': Font(name='Calibri', size=12, bold=True, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_SECUNDARIO, end_color=COLOR_SECUNDARIO, fill_type="solid"),
            'alignment': Alignment(horizontal="center", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
        'encabezado_tabla': {
            'font': Font(name='Calibri', size=11, bold=True, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_ENCABEZADO, end_color=COLOR_ENCABEZADO, fill_type="solid"),
            'alignment': Alignment(horizontal="center", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
        # Datos normales
        'celda_datos': {
            'font': Font(name='Calibri', size=10, color=COLOR_TEXTO_OSCURO),
            'alignment': Alignment(horizontal="center", vertical="center"),
            'border': borde_delgado
        },
        # Filas alternas (para mejor legibilidad)
        'celda_datos_alterna': {
            'font': Font(name='Calibri', size=10, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_FONDO_CLARO, end_color=COLOR_FONDO_CLARO, fill_type="solid"),
            'alignment': Alignment(horizontal="center", vertical="center"),
            'border': borde_delgado
        },
        # Encabezado de sección (responsable)
        'encabezado_responsable': {
            'font': Font(name='Calibri', size=12, bold=True, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_ENCABEZADO_SECCION, end_color=COLOR_ENCABEZADO_SECCION, fill_type="solid"),
            'alignment': Alignment(horizontal="left", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
        # Estilos para información general
        'etiqueta': {
            'font': Font(name='Calibri', size=11, bold=True, color=COLOR_TEXTO_OSCURO),
            'alignment': Alignment(horizontal="left", vertical="center"),
            'border': borde_delgado
        },
        'info_valor': {
            'font': Font(name='Calibri', size=11, color=COLOR_TEXTO_OSCURO),
            'alignment': Alignment(horizontal="left", vertical="center"),
            'border': borde_delgado
        },
        'encabezado_seccion': {
            'font': Font(name='Calibri', size=12, bold=True, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_ENCABEZADO_SECCION, end_color=COLOR_ENCABEZADO_SECCION, fill_type="solid"),
            'alignment': Alignment(horizontal="center", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
        # Para datos alineados a la izquierda
        'dato_izquierda': {
            'font': Font(name='Calibri', size=10, color=COLOR_TEXTO_OSCURO),
            'alignment': Alignment(horizontal="left", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
        'dato_izquierda_alterna': {
            'font': Font(name='Calibri', size=10, color=COLOR_TEXTO_OSCURO),
            'fill': PatternFill(start_color=COLOR_FONDO_CLARO, end_color=COLOR_FONDO_CLARO, fill_type="solid"),
            'alignment': Alignment(horizontal="left", vertical="center", wrap_text=True),
            'border': borde_delgado
        },
    }

def aplicar_estilo_celda(celda, estilo):
    """Aplica un estilo completo a una celda - igual que en el reporte anterior"""
    if 'font' in estilo:
        celda.font = estilo['font']
    if 'fill' in estilo:
        celda.fill = estilo['fill']
    if 'alignment' in estilo:
        celda.alignment = estilo['alignment']
    if 'border' in estilo:
        celda.border = estilo['border']

def ajustar_ancho_columnas(hoja, anchos_personalizados=None):
    """Ajusta el ancho de las columnas según el contenido - igual que en el reporte anterior"""
    if anchos_personalizados:
        for col, ancho in anchos_personalizados.items():
            if isinstance(col, int):
                col_letter = get_column_letter(col)
            else:
                col_letter = col
            hoja.column_dimensions[col_letter].width = ancho
    else:
        for column in hoja.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            hoja.column_dimensions[column_letter].width = adjusted_width

def ajustar_alto_fila(hoja, fila, altura):
    """Ajusta la altura de una fila específica - igual que en el reporte anterior"""
    hoja.row_dimensions[fila].height = altura

def sanitizar_nombre_hoja(nombre):
    """Limpia el nombre para que sea válido como nombre de hoja en Excel"""
    # Reemplazar caracteres inválidos
    nombre = re.sub(r'[\\/*?:[\]]', '_', nombre)
    # Limitar longitud a 31 caracteres (límite de Excel)
    if len(nombre) > 31:
        nombre = nombre[:28] + "..."
    return nombre

# --- Vista Principal del Reporte con estilos mejorados ---

def exportar_bienes_por_responsable_excel(request):
    """
    Genera un reporte en Excel de bienes asignados, agrupados por 
    Subdependencia y luego por Responsable, con una pestaña por cada subdependencia.
    """
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    fecha_descarga = datetime.now().strftime("%Y%m%d_%H%M")
    response['Content-Disposition'] = f'attachment; filename="reporte_bienes_responsables_{fecha_descarga}.xlsx"'

    # OPCIÓN 1: Filtro simple usando el campo 'devuelto' que mencionaste anteriormente
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
        # Crear una hoja con mensaje de que no hay datos con estilos del reporte anterior
        ws = wb.create_sheet(title="Sin Datos")
        ws.sheet_view.showGridLines = False
        
        # Título principal - con estilos del reporte anterior
        ws['A1'] = "REPORTE DE BIENES POR RESPONSABLE"
        ws.merge_cells('A1:F1')
        aplicar_estilo_celda(ws['A1'], estilos['titulo_principal'])
        ajustar_alto_fila(ws, 1, 35)
        
        # Mensaje principal
        ws['A3'] = "No hay bienes asignados para mostrar"
        ws.merge_cells('A3:F3')
        celda_mensaje = ws['A3']
        celda_mensaje.font = Font(name='Calibri', size=14, color=COLOR_TEXTO_OSCURO)
        celda_mensaje.alignment = Alignment(horizontal="center", vertical="center")
        
        # Información adicional
        ws['A5'] = "Fecha de generación:"
        aplicar_estilo_celda(ws['A5'], estilos['etiqueta'])
        
        ws['B5'] = datetime.now().strftime("%d/%m/%Y %H:%M")
        aplicar_estilo_celda(ws['B5'], estilos['info_valor'])
        
        # Ajustar anchos
        ajustar_ancho_columnas(ws, {
            'A': 25,
            'B': 30,
            'C': 15,
            'D': 15,
            'E': 15,
            'F': 15
        })
        
        # Ajustar alturas
        ajustar_alto_fila(ws, 1, 35)
        ajustar_alto_fila(ws, 3, 30)
        
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
        
        # Configurar ancho de columnas (6 columnas)
        ajustar_ancho_columnas(ws, {
            1: 20,   # Código
            2: 25,   # Tipo
            3: 20,   # Marca
            4: 20,   # Modelo
            5: 25,   # Serial
            6: 20,   # Condición
        })
        
        # Título de Subdependencia - con estilos del reporte anterior
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        ws.merge_cells(f'A{row_num}:F{row_num}')
        ws.cell(row=row_num, column=1).value = f"REPORTE DE BIENES POR RESPONSABLE - {subdependencia.nombre.upper()} - {fecha_actual}"
        aplicar_estilo_celda(ws.cell(row=row_num, column=1), estilos['titulo_principal'])
        ajustar_alto_fila(ws, row_num, 35)
        row_num += 2  # Espacio después del título
        
        # 5. Agrupar por Responsable (nivel anidado)
        for responsable, grupo_resp in datos['responsables'].items():
            
            # Subtítulo del Responsable - con estilos del reporte anterior
            ws.merge_cells(f'A{row_num}:F{row_num}')
            ws.cell(row=row_num, column=1).value = f"RESPONSABLE: {responsable.nombres_apellidos.upper()}"
            aplicar_estilo_celda(ws.cell(row=row_num, column=1), estilos['encabezado_seccion'])
            ajustar_alto_fila(ws, row_num, 25)
            row_num += 1

            # Encabezados de la tabla de bienes - con estilos del reporte anterior
            cabeceras = ['CÓDIGO', 'TIPO', 'MARCA', 'MODELO', 'SERIAL', 'CONDICIÓN']
            for col_num, cabecera in enumerate(cabeceras, 1):
                celda = ws.cell(row=row_num, column=col_num)
                celda.value = cabecera
                aplicar_estilo_celda(celda, estilos['encabezado_tabla'])
            ajustar_alto_fila(ws, row_num, 25)
            row_num += 1

            # Escribir los bienes del responsable - con estilos alternados como en el reporte anterior
            for idx, detalle in enumerate(grupo_resp):
                # Determinar estilo de fila (alternado como en el reporte anterior)
                estilo_fila = estilos['celda_datos_alterna'] if idx % 2 == 0 else estilos['celda_datos']
                estilo_fila_izquierda = estilos['dato_izquierda_alterna'] if idx % 2 == 0 else estilos['dato_izquierda']
                
                datos_fila_original = [
                    detalle.bien.codigo_bien,
                    detalle.bien.tipo_bien.nombre if detalle.bien.tipo_bien else "Sin especificar",
                    detalle.bien.marca.nombre if detalle.bien.marca else "Sin especificar",
                    detalle.bien.modelo.nombre if detalle.bien.modelo else "Sin especificar",
                    detalle.bien.serial if detalle.bien.serial else "Sin serial",
                    detalle.bien.condicion.nombre if detalle.bien.condicion else "Sin especificar"
                ]
                
                # Aplicar estilos a cada celda
                for col_num, dato in enumerate(datos_fila_original, 1):
                    celda = ws.cell(row=row_num, column=col_num)
                    celda.value = str(dato) if dato else "Sin datos"
                    
                    # Aplicar estilo según el tipo de dato
                    if col_num == 1:  # Código - centrado
                        aplicar_estilo_celda(celda, estilo_fila)
                    else:  # Resto de columnas - alineadas a la izquierda
                        aplicar_estilo_celda(celda, estilo_fila_izquierda)
                
                row_num += 1
            
            # Espacio después de cada responsable (2 filas como en el reporte anterior)
            row_num += 2
        
        # Ajustar altura de filas automáticamente
        for row in range(1, row_num + 1):
            if ws.row_dimensions[row].height is None or ws.row_dimensions[row].height < 20:
                ws.row_dimensions[row].height = 20

    # 7. Crear una hoja de índice/resumen si hay más de una subdependencia
    if len(datos_por_subdependencia) > 1:
        ws_indice = wb.create_sheet(title="Índice")
        ws_indice.sheet_view.showGridLines = False
        
        # Configurar ancho de columnas para el índice
        ajustar_ancho_columnas(ws_indice, {
            1: 8,   # No.
            2: 50,  # Subdependencia
            3: 20,  # Total Responsables
            4: 20,  # Total Bienes
        })
        
        # Título del índice - con estilos del reporte anterior
        ws_indice['A1'] = "ÍNDICE DE SUBDEPENDENCIAS"
        ws_indice.merge_cells('A1:D1')
        aplicar_estilo_celda(ws_indice['A1'], estilos['titulo_principal'])
        ajustar_alto_fila(ws_indice, 1, 35)
        
        row_indice = 3
        
        # Encabezados del índice - con estilos del reporte anterior
        encabezados_indice = ["No.", "SUBDEPENDENCIA", "TOTAL RESPONSABLES", "TOTAL BIENES"]
        for col_num, encabezado in enumerate(encabezados_indice, 1):
            celda = ws_indice.cell(row=row_indice, column=col_num)
            celda.value = encabezado
            aplicar_estilo_celda(celda, estilos['encabezado_tabla'])
        ajustar_alto_fila(ws_indice, row_indice, 25)
        row_indice += 1
        
        # Listar todas las subdependencias con hipervínculos
        for idx, (subdependencia, datos) in enumerate(datos_por_subdependencia.items(), 1):
            nombre_hoja = sanitizar_nombre_hoja(subdependencia.nombre)
            
            # Calcular total de bienes para esta subdependencia
            total_bienes = sum(len(grupo) for grupo in datos['responsables'].values())
            
            # Determinar estilo de fila alternado
            estilo_fila = estilos['celda_datos_alterna'] if idx % 2 == 0 else estilos['celda_datos']
            
            # Número
            celda_numero = ws_indice.cell(row=row_indice, column=1)
            celda_numero.value = idx
            aplicar_estilo_celda(celda_numero, estilo_fila)
            
            # Nombre con hipervínculo (estilo de enlace como en el reporte anterior)
            celda_nombre = ws_indice.cell(row=row_indice, column=2)
            celda_nombre.value = subdependencia.nombre
            celda_nombre.hyperlink = f"#{nombre_hoja}!A1"
            celda_nombre.font = Font(name='Calibri', size=10, color="2563EB", underline="single")
            celda_nombre.fill = estilo_fila['fill'] if 'fill' in estilo_fila else None
            celda_nombre.alignment = Alignment(horizontal="left", vertical="center")
            celda_nombre.border = estilos['celda_datos']['border']
            
            # Total de responsables
            celda_responsables = ws_indice.cell(row=row_indice, column=3)
            celda_responsables.value = len(datos['responsables'])
            aplicar_estilo_celda(celda_responsables, estilo_fila)
            
            # Total de bienes
            celda_bienes = ws_indice.cell(row=row_indice, column=4)
            celda_bienes.value = total_bienes
            aplicar_estilo_celda(celda_bienes, estilo_fila)
            
            row_indice += 1
        
        # Ajustar altura de filas del índice
        for row in range(1, row_indice + 1):
            if ws_indice.row_dimensions[row].height is None or ws_indice.row_dimensions[row].height < 20:
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
    
    # 9. HOJA DE RESUMEN - Similar al reporte anterior
    ws_resumen = wb.create_sheet(title="Resumen")
    
    # Configurar ancho de columnas para resumen
    ajustar_ancho_columnas(ws_resumen, {
        1: 35,  # Etiqueta
        2: 20,  # Valor
    })
    
    # Título de resumen - con estilos del reporte anterior
    ws_resumen['A1'] = "RESUMEN GENERAL DE BIENES POR RESPONSABLE"
    ws_resumen.merge_cells('A1:B1')
    aplicar_estilo_celda(ws_resumen['A1'], estilos['titulo_principal'])
    ajustar_alto_fila(ws_resumen, 1, 35)
    
    # Estadísticas generales
    total_subdependencias = len(datos_por_subdependencia)
    total_responsables = sum(len(datos['responsables']) for datos in datos_por_subdependencia.values())
    total_bienes_general = sum(
        sum(len(grupo) for grupo in datos['responsables'].values()) 
        for datos in datos_por_subdependencia.values()
    )
    
    datos_resumen = [
        ("Total de Subdependencias", total_subdependencias),
        ("Total de Responsables", total_responsables),
        ("Total de Bienes Asignados", total_bienes_general),
        ("", ""),
        ("Fecha de generación", datetime.now().strftime("%d/%m/%Y %H:%M"))
    ]
    
    fila_resumen = 3
    for etiqueta, valor in datos_resumen:
        if etiqueta:  # Si no es fila vacía
            # Etiqueta
            celda_etiqueta = ws_resumen.cell(row=fila_resumen, column=1, value=etiqueta)
            aplicar_estilo_celda(celda_etiqueta, estilos['etiqueta'])
            
            # Valor
            celda_valor = ws_resumen.cell(row=fila_resumen, column=2, value=valor)
            aplicar_estilo_celda(celda_valor, estilos['info_valor'])
        
        fila_resumen += 1
    
    # Mover la hoja resumen después del índice (si existe) o al principio
    if "Índice" in wb.sheetnames:
        # Mover resumen después del índice
        resumen_sheet = wb["Resumen"]
        idx_resumen = wb._sheets.index(resumen_sheet)
        idx_indice = wb._sheets.index(wb["Índice"])
        if idx_resumen > idx_indice:
            wb._sheets.insert(idx_indice + 1, wb._sheets.pop(idx_resumen))
    else:
        # Si no hay índice, mover resumen al principio
        resumen_sheet = wb["Resumen"]
        wb._sheets.insert(0, wb._sheets.pop(wb._sheets.index(resumen_sheet)))
    
    # 10. Asegurar que haya al menos una hoja visible y activa
    if len(wb.sheetnames) == 0:
        # Crear una hoja por defecto si por alguna razón no hay hojas
        ws = wb.create_sheet(title="Reporte")
        ws['A1'] = "Reporte Generado"
        aplicar_estilo_celda(ws['A1'], estilos['titulo_principal'])
        ws.merge_cells('A1:F1')
        ajustar_alto_fila(ws, 1, 35)
    
    # Establecer la primera hoja como activa
    wb.active = wb.worksheets[0]
    
    wb.save(response)
    return response