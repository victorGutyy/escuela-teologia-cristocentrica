# -*- coding: utf-8 -*-
"""
Plantilla reutilizable para generar los PDF de la Escuela de Teología
Cristocéntrica con estilo visual consistente entre entregas.

Uso (desde el agente, cada semana):

    from build_pdf import generar_pdf, Seccion

    generar_pdf(
        ruta_salida="entregas/EscuelaTeologia_S2_ENSENANZA_la-unicidad-de-dios.pdf",
        tipo="Enseñanza",              # "Doctrina" | "Enseñanza"
        semana=2,
        titulo_tema="LA UNICIDAD DE DIOS",
        texto_base='"Oye, Israel: Jehová nuestro Dios, Jehová uno es." — Deuteronomio 6:4',
        introduccion="<p con texto...>",
        desarrollo=[
            Seccion("A. Subtítulo", "<párrafo(s) HTML simple: <b>, <i>, &ldquo;&rdquo;, &mdash;>"),
            Seccion("B. Subtítulo", "..."),
        ],
        ejemplo_biblico_titulo="3. Ejemplo bíblico: ...",
        ejemplo_biblico_texto="...",
        ejemplo_actual_texto="...",
        reflexion_pastoral_texto="...",
        preguntas=["¿Pregunta 1?", "¿Pregunta 2?", "¿Pregunta 3?", "¿Pregunta 4?"],
        referencias=["Deuteronomio 6:4 — ...", "Isaías 44:6 — ..."],
    )

Todos los campos de texto admiten el subconjunto de XML de reportlab
(<b>, <i>, <br/>, entidades &ldquo; &rdquo; &mdash; &hellip; &bull;) — NO usar
HTML completo. Mantener los párrafos como un solo string (usar <br/><br/> si se
necesitan varios párrafos dentro de una misma sección).

Requiere: pip install reportlab
"""
from dataclasses import dataclass
from typing import List

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem,
)


@dataclass
class Seccion:
    subtitulo: str
    texto: str


def _estilos():
    base = getSampleStyleSheet()
    return {
        "subtitle": ParagraphStyle(
            "SubtitleCustom", parent=base["Normal"], fontName="Helvetica",
            fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=4,
            textColor=colors.HexColor("#555555"),
        ),
        "title": ParagraphStyle(
            "TitleCustom", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=2,
            textColor=colors.HexColor("#1a2a4a"),
        ),
        "base_text": ParagraphStyle(
            "BaseText", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=10.5, leading=14, alignment=TA_CENTER, spaceAfter=14,
            textColor=colors.HexColor("#7a1f1f"),
        ),
        "h1": ParagraphStyle(
            "H1Custom", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=13, leading=16, spaceBefore=10, spaceAfter=6,
            textColor=colors.HexColor("#1a2a4a"),
        ),
        "h2": ParagraphStyle(
            "H2Custom", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, spaceBefore=6, spaceAfter=4,
            textColor=colors.HexColor("#2f4a7a"),
        ),
        "body": ParagraphStyle(
            "BodyCustom", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.7, leading=13.2, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "pastor": None,  # se arma abajo a partir de "body"
        "question": None,
        "ref": ParagraphStyle(
            "RefCustom", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.3, leading=11, spaceAfter=2,
        ),
        "footer": ParagraphStyle(
            "FooterCustom", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=8, leading=10, alignment=TA_CENTER,
            textColor=colors.HexColor("#888888"), spaceBefore=10,
        ),
    }


def generar_pdf(
    ruta_salida: str,
    tipo: str,
    semana: int,
    titulo_tema: str,
    texto_base: str,
    introduccion: str,
    desarrollo: List[Seccion],
    ejemplo_biblico_titulo: str,
    ejemplo_biblico_texto: str,
    ejemplo_actual_texto: str,
    reflexion_pastoral_texto: str,
    preguntas: List[str],
    referencias: List[str],
):
    styles = _estilos()
    styles["pastor"] = ParagraphStyle(
        "PastorCustom", parent=styles["body"], textColor=colors.HexColor("#2a2a2a"),
        backColor=colors.HexColor("#f6f1e4"), borderPadding=8, spaceAfter=6,
    )
    styles["question"] = ParagraphStyle(
        "QuestionCustom", parent=styles["body"], spaceAfter=5,
    )

    story = []
    story.append(Paragraph("Escuela de Teología Cristocéntrica", styles["subtitle"]))
    story.append(Paragraph("Doctrina Unicitaria del Nombre de Jesús", styles["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#c9a24a"),
                             spaceBefore=4, spaceAfter=10))
    story.append(Paragraph(titulo_tema.upper(), styles["title"]))
    story.append(Paragraph(f"Entrega de {tipo} &mdash; Semana {semana}", styles["subtitle"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(texto_base, styles["base_text"]))

    story.append(Paragraph("1. Introducción", styles["h1"]))
    story.append(Paragraph(introduccion, styles["body"]))

    story.append(Paragraph("2. Desarrollo doctrinal", styles["h1"]))
    for sec in desarrollo:
        story.append(Paragraph(sec.subtitulo, styles["h2"]))
        story.append(Paragraph(sec.texto, styles["body"]))

    story.append(Paragraph(ejemplo_biblico_titulo, styles["h1"]))
    story.append(Paragraph(ejemplo_biblico_texto, styles["body"]))

    story.append(Paragraph("4. Ejemplo de vida actual", styles["h1"]))
    story.append(Paragraph(ejemplo_actual_texto, styles["body"]))

    story.append(Paragraph("5. Reflexión pastoral y aplicación práctica", styles["h1"]))
    story.append(Paragraph(reflexion_pastoral_texto, styles["pastor"]))

    story.append(Paragraph("6. Preguntas de estudio", styles["h1"]))
    story.append(ListFlowable(
        [ListItem(Paragraph(p, styles["question"])) for p in preguntas],
        bulletType="1", leftIndent=18,
    ))

    story.append(Paragraph("7. Referencias bíblicas citadas", styles["h1"]))
    for r in referencias:
        story.append(Paragraph("&bull; " + r, styles["ref"]))

    story.append(Paragraph(
        "Escuela de Teología Cristocéntrica &mdash; Material preparado para edificación "
        "congregacional. La obra de transformación espiritual pertenece al Espíritu Santo; "
        "este documento es solo un instrumento.",
        styles["footer"],
    ))

    doc = SimpleDocTemplate(
        ruta_salida, pagesize=letter,
        topMargin=1.6 * cm, bottomMargin=1.6 * cm, leftMargin=2.0 * cm, rightMargin=2.0 * cm,
        title=f"{titulo_tema} - {tipo} S{semana}",
        author="Escuela de Teologia Cristocentrica",
    )
    doc.build(story)
    return ruta_salida
