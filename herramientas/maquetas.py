"""Maquetas de alta fidelidad en SVG (antes / después) para el laboratorio visual."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "figuras"
F = 'font-family="Source Sans 3, Helvetica, Arial, sans-serif"'
def svg(n, c): (OUT / f"{n}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 640" width="360" height="640" {F}><rect x="1" y="1" width="358" height="638" rx="28" fill="#fff" stroke="#0b0b0b" stroke-width="2"/>{c}</svg>', encoding="utf-8")
def r(x, y, w, h, f, rx=8, st=None): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}"' + (f' stroke="{st}" stroke-width="1.5"' if st else "") + "/>"
def t(x, y, s, size=14, c="#0b0b0b", w="400", a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{w}" text-anchor="{a}">{s}</text>'
# Antes: poco contraste, sin jerarquía, iconos mezclados, espaciado irregular
c = r(1, 1, 358, 90, "#6BCB77", 28) + t(180, 58, "Sala 2.14", 16, "#ffffff", "400", "middle")
c += r(12, 100, 336, 120, "#d9d8d4", 2) + t(20, 240, "Sala de trabajo en grupo 2.14 · Biblioteca de Getafe · planta 2 · capacidad 6 personas · pizarra · enchufes", 9.5, "#9a9a9a")
c += t(20, 262, "DISPONIBILIDAD", 15, "#0b0b0b", "700") + "".join(r(20 + k*27, 270, 22, 28, "#8fd694" if k not in (2, 3, 7) else "#f28b82", 2) for k in range(12))
c += f'<circle cx="30" cy="330" r="9" fill="#0b0b0b"/><rect x="60" y="321" width="18" height="18" fill="none" stroke="#2a78d6" stroke-width="3"/><path d="M100 339 L109 321 L118 339 Z" fill="#eda100"/>'
c += t(20, 370, "Puedes reservar esta sala durante un máximo de dos horas al día y debes confirmar tu llegada en los primeros quince minutos o la reserva se cancelará automáticamente.", 9, "#bbbbbb")
c += r(20, 420, 150, 44, "#6BCB77", 4) + t(95, 447, "Reservar", 15, "#ffffff", "400", "middle") + r(190, 420, 150, 44, "#6BCB77", 4) + t(265, 447, "Cancelar", 15, "#ffffff", "400", "middle")
svg("m_antes", c)
# Después: contraste AA, jerarquía, iconos coherentes, escala de 8 px
c = r(1, 1, 358, 90, "#1c6b3a", 28) + t(28, 62, "‹", 24, "#ffffff") + t(180, 62, "Sala 2.14", 17, "#ffffff", "600", "middle")
c += r(16, 104, 328, 132, "#e7efe9", 12) + t(180, 176, "Foto de la sala", 13, "#52514e", "400", "middle")
c += t(24, 268, "Sala de trabajo en grupo 2.14", 19, "#0b0b0b", "600") + t(24, 292, "Biblioteca de Getafe · planta 2", 14, "#52514e")
c += "".join(r(24 + i*104, 308, 96, 32, "#f1f3f1", 16) + t(72 + i*104, 329, s, 13, "#0b0b0b", "400", "middle") for i, s in enumerate(["6 personas", "Pizarra", "Enchufes"]))
c += t(24, 372, "Disponibilidad hoy", 16, "#0b0b0b", "600") + "".join(r(24 + k*26, 384, 24, 32, "#1c6b3a" if k not in (2, 3, 7) else "#ffffff", 4, None if k not in (2, 3, 7) else "#8a8a8a") for k in range(12))
c += t(24, 436, "9 h", 12, "#52514e") + t(336, 436, "21 h", 12, "#52514e", "400", "end") + r(24, 450, 12, 12, "#1c6b3a", 3) + t(42, 461, "Libre", 13, "#0b0b0b") + r(96, 450, 12, 12, "#fff", 3, "#8a8a8a") + t(114, 461, "Ocupada", 13, "#0b0b0b")
c += t(24, 494, "Máximo 2 horas al día. Confirma tu llegada en 15 min.", 13, "#52514e")
c += r(24, 528, 312, 48, "#1c6b3a", 10) + t(180, 558, "Reservar 16:00–18:00", 16, "#ffffff", "600", "middle") + t(180, 604, "Ver otras salas", 14, "#1c6b3a", "600", "middle")
svg("m_despues", c)
print("ok")
