# apps/gestion/services.py

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.graphics.shapes import Drawing, Rect, Line
from reportlab.graphics import renderPDF
from django.utils import timezone
import os
from apps.gestion.utils.acta_prestamo import header_footer_combined 





class ActaPrestamoService:
    """
    Servicio para generar el PDF del Acta de Préstamo de un Prestamo específico.
    """

    def __init__(
        self,
        prestamo_instance,
        director_general="------------------",
        cedula_director="V- -------------",
        directora_zona="--------------",
        cedula_directora_zona="V- ------------"
    ):
        self.prestamo = prestamo_instance
        self.director_general = director_general
        self.cedula_director = cedula_director
        self.directora_zona = directora_zona
        self.cedula_directora_zona = cedula_directora_zona

        self.styles = getSampleStyleSheet()
        
        # Estilo para el título principal
        self.styles.add(ParagraphStyle(
            name='TituloFormal',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.Color(0.15, 0.15, 0.15),  # Gris muy oscuro
            alignment=1,  # Centrado
            spaceAfter=24,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=8
        ))
        
        # Estilo para subtítulos institucionales
        self.styles.add(ParagraphStyle(
            name='SubtituloFormal',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.Color(0.25, 0.25, 0.25),  # Gris oscuro
            alignment=1,
            spaceAfter=12,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para información institucional
        self.styles.add(ParagraphStyle(
            name='InfoInstitucional',
            fontSize=11,
            textColor=colors.Color(0.35, 0.35, 0.35),  # Gris medio
            alignment=1,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Estilo justificado mejorado
        self.styles.add(ParagraphStyle(
            name='JustifyFormal', 
            parent=self.styles['Normal'],
            alignment=4,  # Justify
            fontSize=11,
            textColor=colors.Color(0.1, 0.1, 0.1),  # Gris muy oscuro
            leading=16,
            spaceAfter=10,
            spaceBefore=5,
            fontName='Helvetica'
        ))
        
        # Estilo para el footer
        self.styles.add(ParagraphStyle(
            name='FooterStyle',
            fontSize=8,
            textColor=colors.Color(0.5, 0.5, 0.5),  # Gris medio
            alignment=1,
            fontName='Helvetica',
            leading=10
        ))



    def _generar_encabezado_formal(self):
        """Genera un encabezado formal con banner y información institucional."""
        story = []
        
        # Título principal con más prominencia
        story.append(Paragraph(
            "<b>ACTA DE PRÉSTAMO</b>", 
            self.styles['TituloFormal']
        ))
        story.append(Spacer(1, 0.35 * inch))

        # Texto introductorio mejorado
        texto_intro = f"""
        En la ciudad de Caracas, constituidos los ciudadanos <b>{self.director_general}</b>,
        Cédula de Identidad N.º {self.cedula_director}, Director General de la Oficina de Tecnología de la Información y la Comunicación, según Resolución DM/N° ----- de fecha -------,
        Publicado en la Gaceta Oficial N.º -------, de fecha --------- y <b>{self.directora_zona}</b>,
        Cédula de Identidad Nº {self.cedula_directora_zona}, Directora de la Zona Educativa del Distrito Capital,
        Resolución N°. DM/N° ------- de fecha --------- Publicado en la Gaceta Oficial N°------de fecha ----------
        hacemos constar por medio de la presente Acta, que a partir de esta fecha, la Dirección General de la Oficina de Tecnología de la Información y la Comunicación procede a entregar
        en calidad de préstamo por () mes a la <b>{self.prestamo.departamento_recibe.nombre}</b>,
        ubicada en piso --- de este Ministerio, para su uso y custodia los Bienes Públicos que se especifican a continuación:
        """
        story.append(Paragraph(texto_intro, self.styles['JustifyFormal']))
        story.append(Spacer(1, 0.3 * inch))
        return story

    def _generar_tabla_bienes_formal(self):
        """Genera la tabla con los detalles de los bienes con diseño formal."""
        data = [['Cantidad', 'Descripción', 'Valor Unitario', 'Valor Total']]
        valor_total_general = 0

        detalles = self.prestamo.detalles.select_related('bien').all()

        for detalle in detalles:
            bien = detalle.bien
            cantidad = getattr(detalle, 'cantidad', 1)
            descripcion = f"{bien.categoria} - {bien.modelo or ''} - {bien.caracteristicas or ''}"
            valor_unitario = bien.valor_unitario or 0
            valor_total_item = valor_unitario * cantidad
            valor_total_general += valor_total_item
            data.append([cantidad, descripcion, f"Bs. {valor_unitario:,.2f}", f"Bs. {valor_total_item:,.2f}"])

        # Total
        data.append(['', '', 'Total Bs.', f"Bs. {valor_total_general:,.2f}"])

        table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Encabezado gris más oscuro
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.8, colors.Color(0.4, 0.4, 0.4)),  # Líneas grises más definidas
            ('BOX', (0, 0), (-1, -1), 1.5, colors.Color(0.3, 0.3, 0.3)),  # Borde más prominente
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.Color(0.96, 0.96, 0.96)]),  # Filas alternadas sutiles
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Fila total más destacada
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])

                # En _generar_tabla_bienes_formal
        table = Table(data, colWidths=[0.9 * inch, 3.2 * inch, 1.4 * inch, 1.4 * inch])  # Suma: 6.9
        table.setStyle(table_style)
        return table

    def _generar_firmas_formal(self):
        """Genera la sección de firmas del documento con diseño formal."""
        story = []
        fecha_actual_str = timezone.now().strftime("%d días del mes de %B de %Y")

        texto_cierre = f"""
        Este préstamo provisional será de uso exclusivo de la <b>{self.prestamo.departamento_recibe.nombre}</b> y no podrán ser transferidos a ningún otro ente en particular, ya que están incluidos en el inventario de la Dirección General de la Oficina de Tecnología de la Información y la Comunicación, de igual forma tendrán la obligación de mantener los equipos en perfectas condiciones de uso.
        A tales efectos se levanta la presente acta por duplicado en la ciudad de Caracas, a los {fecha_actual_str}.
        """
        story.append(Paragraph(texto_cierre, self.styles['JustifyFormal']))
        story.append(Spacer(1, 0.5 * inch))

        firmas_data = [
            ['<b>Unidad que Entrega:</b>', '<b>Unidad que Recibe:</b>'],
            ['', ''],
            ['', ''],
            ['', ''],
            ['_____________________________', '_____________________________'],
            ['C.I. V- _______________', 'C.I. V- _______________'],
            ['<b>Director General de la Oficina de</b>', '<b>Director de la Zona Educativa</b>'],
            ['<b>Tecnología de la Información y la Comunicación</b>', '<b>del Distrito Capital</b>'],
            ['', ''],
            ['', ''],
            ['<b>Testigo Unidad que Entrega:</b>', '<b>Testigo Unidad que Recibe:</b>'],
            ['', ''],
            ['_____________________________', '_____________________________'],
            ['C.I. N° V- _______________', 'C.I. V- _______________'],
            ['<b>Registrador de Bienes Públicos</b>', '<b>Registrador de Bienes Públicos</b>']
        ]
        
        firmas_table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.Color(0.2, 0.2, 0.2)),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ])
        
        firmas_table = Table(firmas_data, colWidths=[3.75 * inch, 3.75 * inch])
        firmas_table.setStyle(firmas_table_style)
        story.append(firmas_table)
        return story



    def generar_pdf(self, response):
        """Método público que orquesta la generación del PDF con diseño formal."""
        doc = SimpleDocTemplate(
            response, 
            pagesize=letter,
            topMargin=1.5 * inch,
            bottomMargin=2.0 * inch,
            leftMargin=0.8 * inch,
            rightMargin=0.8 * inch
        )
        
        story = []
        story.extend(self._generar_encabezado_formal())
        story.append(self._generar_tabla_bienes_formal())
        story.append(Spacer(1, 0.4 * inch))
        story.extend(self._generar_firmas_formal())
        
        doc.build(story, onFirstPage=header_footer_combined, onLaterPages=header_footer_combined)
