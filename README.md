# Escuela de Teología Cristocéntrica

Repositorio de continuidad para las entregas semanales de la Escuela de Teología
(Doctrina Unicitaria del Nombre de Jesús). Un agente en la nube (rutina programada,
todos los lunes 8:00 AM hora de Bogotá) lee este repositorio, genera la entrega de
la semana en PDF y la deja commiteada aquí, lista para que un humano la suba
manualmente a Google Drive y la comparta en Google Classroom.

## Cómo funciona la continuidad

Cada ejecución del agente arranca sin memoria de ejecuciones anteriores (es una
sesión en la nube aislada). Por eso el estado vive en archivos versionados aquí,
no en la conversación:

- **[`PROMPT_MAESTRO.md`](PROMPT_MAESTRO.md)** — las reglas de contenido, estructura
  obligatoria y formato de salida que debe seguir *cada* entrega. Es la fuente de
  verdad doctrinal/editorial. Editar este archivo cambia el comportamiento de todas
  las entregas futuras sin tocar la rutina programada.
- **[`ESTADO.md`](ESTADO.md)** — historial de entregas ya generadas: número de
  semana, tipo (Doctrina/Enseñanza), tema, fecha y archivo. El agente lo lee para
  saber cuál es el siguiente número de semana y qué tipo toca (alternan).
- **[`ROADMAP.md`](ROADMAP.md)** — currículo ordenado de doctrinas y enseñanzas
  fundamentales. El agente marca cada tema como cubierto (`[x]`) al usarlo y toma
  el primer tema `[ ]` pendiente para la siguiente entrega. Si la lista se agota,
  añade un nuevo tema fundamental alineado a la doctrina antes de continuar.
- **[`entregas/`](entregas)** — los PDF ya generados, uno por semana.
- **[`scripts/build_pdf.py`](scripts/build_pdf.py)** — plantilla reutilizable en
  Python (reportlab) que produce el PDF con el formato visual estándar de la
  escuela. El agente la importa y le pasa el contenido de la semana; no debería
  reinventar el diseño cada vez.

## Flujo de cada ejecución automática

1. Leer `ESTADO.md` → determinar semana N+1 y alternar el tipo respecto a la última entrega.
2. Leer `ROADMAP.md` → tomar el primer tema pendiente (o proponer uno nuevo si no queda ninguno).
3. Redactar el contenido siguiendo al pie de la letra `PROMPT_MAESTRO.md`.
4. Generar el PDF con `scripts/build_pdf.py`, guardarlo en `entregas/`.
5. Actualizar `ESTADO.md` (nueva fila) y `ROADMAP.md` (marcar tema usado).
6. Commit y push a `main`.

La subida a Google Drive/Google Classroom queda manual, por diseño.
