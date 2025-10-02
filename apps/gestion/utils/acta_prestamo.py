from reportlab.platypus      import Table, TableStyle, Paragraph,  Image, KeepTogether, Spacer
from reportlab.lib          import colors
from reportlab.lib.styles   import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums    import TA_JUSTIFY
import os
from django.conf import settings
import datetime
from reportlab.lib.pagesizes             import letter
from reportlab.platypus.flowables        import Flowable
from reportlab.graphics.shapes           import Drawing, Rect, String
from reportlab.graphics.charts.legends   import Legend
from reportlab.graphics.charts.piecharts import Pie


 
   
    


def header_banner(canvas, doc):
    canvas.saveState()
    # Ruta a tu imagen de banner (asegúrate de que la ruta sea correcta)
    banner_path = os.path.join(settings.STATIC_ROOT, 'img', 'membrete.png')
    try:
        img = Image(banner_path)
        # Calcula la posición X para centrar la imagen en el ancho disponible (512 puntos)
        # Asumiendo que el margen izquierdo es de 50 puntos y el ancho de página es letter[0] (612 puntos)
        # El ancho de la imagen debe ser 512 puntos
         # Dimensiones originales de la imagen en píxeles
        original_pixel_width = 1181
        original_pixel_height = 148

        # Calcula la relación de aspecto directamente desde los píxeles
        aspect_ratio = original_pixel_height / original_pixel_width
        # Calcula la nueva altura manteniendo la proporción
        new_height_points = 512 * aspect_ratio
        img_width = 512
        img_height = new_height_points # Altura de tu banner, ajusta según sea necesario
        
        img.drawWidth = img_width
        img.drawHeight = img_height

        # Posición X: Margen izquierdo (50)
        # Posición Y: Parte superior de la página menos la altura del banner y un pequeño margen
        y_position = letter[1] - img_height - 30 # letter[1] es la altura de la página (792 para letter)
        x_position = 50 # El margen izquierdo que especificaste

        img.wrapOn(canvas, img_width, img_height) # Necesario para que ReportLab calcule las dimensiones
        img.drawOn(canvas, x_position, y_position)
    except FileNotFoundError:
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(50, letter[1] - 50, "ERROR: Banner no encontrado")
    canvas.restoreState()


def footer_fijo(canvas, doc):
    """
    Función para crear un footer fijo en todas las páginas
    """
    canvas.saveState()
    
    # Configurar fuente y tamaño para el footer
    canvas.setFont('Helvetica', 8)
    
    # Obtener dimensiones de la página
    width, height = letter
    
    # Posición Y del footer (desde abajo)
    footer_y = 30
    
    # Línea separadora opcional
    canvas.setStrokeColor(colors.grey)
    canvas.setLineWidth(0.5)
    canvas.line(50, footer_y + 25, width - 50, footer_y + 25)
    
    # Texto del footer - lado izquierdo
    canvas.setFillColor(colors.grey)
    fecha_generacion = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    canvas.drawString(50, footer_y + 10, f"Generado: {fecha_generacion}")
    
    # Texto del footer - centro
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(colors.Color(0.2, 0.3, 0.5))
    footer_center = "Acta de Préstamo"
    text_width = canvas.stringWidth(footer_center, 'Helvetica-Bold', 8)
    canvas.drawString((width - text_width) / 2, footer_y + 10, footer_center)
    
    # Número de página - lado derecho
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    page_num = f"Página {doc.page}"
    page_width = canvas.stringWidth(page_num, 'Helvetica', 8)
    canvas.drawString(width - 50 - page_width, footer_y + 10, page_num)
    
    # Copyright en la línea inferior
    canvas.setFont('Helvetica', 7)
    copyright_text = "©2025 - OTIC • Sistema de Asignacion de bienes"
    copyright_width = canvas.stringWidth(copyright_text, 'Helvetica', 7)
    canvas.drawString((width - copyright_width) / 2, footer_y - 5, copyright_text)
    
    canvas.restoreState()

def header_footer_combined(canvas, doc):
    """
    Función combinada que aplica tanto header como footer
    """
    header_banner(canvas, doc)
    footer_fijo(canvas, doc)


