"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
Los valores se calculan con las mismas fórmulas que las funciones del libro (datos/funciones_ux.R).
"""
import math, pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": GRIS, "axes.labelcolor": TINTA2, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc, linespacing=1.15, fontweight=peso)


def flecha(ax, a, b, texto=None, desp=(0, 0), color=TINTA2, rad=0.0, fs=8.5):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=color, lw=1.1,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if texto:
        mx, my = (a[0] + b[0]) / 2 + desp[0], (a[1] + b[1]) / 2 + desp[1]
        ax.text(mx, my, texto, ha="center", va="center", fontsize=fs, color=TINTA2,
                bbox=dict(fc=SUP, ec="none", pad=1))


def wald_ajustado(x, n, z=1.959964):
    na = n + z ** 2; pa = (x + z ** 2 / 2) / na; m = z * math.sqrt(pa * (1 - pa) / na)
    return x / n, max(0, pa - m), min(1, pa + m)



def luminancia(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    l = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ------------------------------------------------------------------ Tema 4
def tema4():
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    y = 0
    for paso in range(-1, 6):
        px = 16 * 1.25 ** paso
        ax.text(0, y, f"{px:.1f} px", fontsize=9, color=TINTA2, va="baseline")
        ax.text(0.95, y, f"{px / 16:.3g} rem", fontsize=9, color=TINTA2, va="baseline")
        ax.text(2.0, y, "Biblioteca", fontsize=px * 0.72, color=S[0] if paso == 0 else TINTA, va="baseline",
                fontweight="bold" if paso >= 3 else "normal")
        if paso == 0:
            ax.text(2.0 + 0.11 * px * 0.72 * 0.95 + 0.4, y, "← texto base", fontsize=9, color=S[0], va="baseline")
        y += px * 0.045 + 0.25
    ax.set_xlim(0, 8); ax.set_ylim(-0.4, y + 0.3); ax.axis("off")
    guardar(fig, "tema4_escala.svg")


# ------------------------------------------------------------------ Tema 5
def tema5():
    pal = {"texto": "#202124", "primario_oscuro": "#174ea6", "texto_secundario": "#5f6368", "exito": "#188038",
           "error": "#d93025", "primario": "#1a73e8", "acento": "#f29900", "borde": "#dadce0"}
    nombres = list(pal); vals = [contraste(pal[n], "#ffffff") for n in nombres]
    orden = sorted(range(len(nombres)), key=lambda i: vals[i])
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    for k, i in enumerate(orden):
        ax.barh(k, vals[i], color=pal[nombres[i]], height=0.62, edgecolor=SUP, linewidth=2)
        ax.text(vals[i] + 0.25, k, f"{vals[i]:.2f}", va="center", fontsize=9, color=TINTA2)
    ax.set_yticks(range(len(orden))); ax.set_yticklabels([nombres[i].replace("_", " ").replace("exito", "éxito") for i in orden], fontsize=9.5)
    for umbral, t, ha, dx in ((3, "3:1 componentes y texto grande", "right", -0.15), (4.5, "4,5:1 texto normal", "left", 0.15)):
        ax.axvline(umbral, color=TINTA2, lw=1, ls="--")
        ax.text(umbral + dx, len(orden) - 0.2, t, fontsize=8.5, color=TINTA2, va="bottom", ha=ha)
    ax.set_xlabel("Contraste con el blanco (relación : 1)"); ax.set_xlim(0, 18.5); ax.set_ylim(-0.6, len(orden) + 0.4)
    ax.grid(axis="x", color="#ecebe8", lw=0.8); ax.set_axisbelow(True)
    guardar(fig, "tema5_contraste.svg")


# ------------------------------------------------------------------ Tema 7
def tema7():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), gridspec_kw={"width_ratios": [12, 8, 4]})
    conf = [("Escritorio · 12 columnas", 12, [(0, 8, 0, "Principal (8)"), (8, 4, 0, "Lateral (4)")]),
            ("Tableta · 8 columnas", 8, [(0, 8, 0, "Principal (8)"), (0, 8, 1, "Lateral (8)")]),
            ("Móvil · 4", 4, [(0, 4, 0, "Principal"), (0, 4, 1, "Lateral")])]
    for ax, (tit, n, mods) in zip(axs, conf):
        for i in range(n):
            ax.add_patch(Rectangle((i + 0.1, 0), 0.8, 4.2, fc="#e9f1fb", ec="none"))
        for x, w, fila, t in mods:
            y = 2.3 - fila * 2.1
            ax.add_patch(FancyBboxPatch((x + 0.1, y), w - 0.2, 1.7, boxstyle="round,pad=0,rounding_size=0.15",
                                        fc=S[0] if "Principal" in t else S[2], ec=SUP, lw=1.5, alpha=0.9))
            ax.text(x + w / 2, y + 0.85, t, ha="center", va="center", fontsize=9, color=SUP, fontweight="bold")
        ax.add_patch(Rectangle((0, 0), n, 4.2, fc="none", ec=TINTA2, lw=1.2))
        ax.set_title(tit, fontsize=9.5, color=TINTA, loc="left")
        ax.set_xlim(-0.1, n + 0.1); ax.set_ylim(-0.1, 4.3); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema7_adaptable.svg")


# ------------------------------------------------------------------ Tema 8
def tema8():
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 4.4))
    def formulario(ax, etiqueta_gap, grupo_gap, boton_gap, titulo):
        y = 9.4
        ax.text(0.3, y, "Reservar una sala", fontsize=11, fontweight="bold", color=TINTA)
        y -= 0.9 if grupo_gap > 0.7 else 0.55
        for i, (et, campo) in enumerate([("Fecha", "12/03/2027"), ("Franja", "16:00 - 18:00"), ("Personas", "3")]):
            ax.text(0.3, y, et, fontsize=8.5, color=TINTA2); y -= etiqueta_gap
            ax.add_patch(Rectangle((0.3, y - 0.55), 5.2, 0.55, fc=SUP, ec="#8a8a86", lw=1))
            ax.text(0.45, y - 0.28, campo, fontsize=8.5, color=TINTA, va="center"); y -= 0.55 + grupo_gap
        y -= boton_gap
        ax.add_patch(FancyBboxPatch((0.3, y - 0.65), 2.2, 0.65, boxstyle="round,pad=0,rounding_size=0.12", fc="#174ea6", ec="none"))
        ax.text(1.4, y - 0.33, "Reservar", fontsize=9, color=SUP, ha="center", va="center", fontweight="bold")
        ax.add_patch(Rectangle((0, 0), 5.8, 10.2, fc="none", ec=GRIS, lw=1))
        ax.set_title(titulo, fontsize=9.5, color=TINTA, loc="left")
        ax.set_xlim(-0.1, 5.9); ax.set_ylim(-0.1, 10.3); ax.set_aspect("equal"); ax.axis("off")
    formulario(axs[0], 0.45, 0.45, 0.0, "Espacio uniforme e insuficiente")
    formulario(axs[1], 0.3, 0.95, 0.6, "Espacio jerarquizado")
    guardar(fig, "tema8_espacio.svg")


# ------------------------------------------------------------------ Tema 9
def tema9():
    fig, ax = plt.subplots(figsize=(9.6, 3.5))
    niveles = ["Átomos", "Moléculas", "Organismos", "Plantillas", "Páginas"]
    ejemplos = ["botón, campo,\netiqueta", "buscador", "cabecera con\nbuscador", "estructura de la\npágina de resultados",
                "resultados con\nlibros reales"]
    x = 0
    for i, (n, e) in enumerate(zip(niveles, ejemplos)):
        w = 1.0 + 0.35 * i; h = 0.9 + 0.45 * i
        caja(ax, x, 0.6, w, h, "", fc=["#dbe8f8", "#b3cdf0", "#7eaae4", "#4a85d3", "#1f5fae"][i], ec=SUP)
        ax.text(x + w / 2, 0.6 + h + 0.25, n, ha="center", fontsize=10, color=TINTA, fontweight="bold")
        ax.text(x + w / 2, 0.35, e, ha="center", va="top", fontsize=8.5, color=TINTA2, linespacing=1.1)
        if i < 4:
            flecha(ax, (x + w + 0.05, 0.6 + h / 2), (x + w + 0.4, 0.6 + h / 2))
        x += w + 0.45
    ax.set_xlim(-0.1, x); ax.set_ylim(-0.7, 3.6); ax.set_aspect("equal"); ax.axis("off")
    guardar(fig, "tema9_atomico.svg")



# ====================================================================== v1.1
def t3_transicion():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, alta in zip(axs, (False, True)):
        ax.set_xlim(0, 100); ax.set_ylim(100, 0); ax.set_aspect("equal"); ax.axis("off")
        borde = TINTA2 if not alta else "#c9cfe0"
        ax.add_patch(FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=0,rounding_size=2", fc=SUP, ec=borde, lw=1.4))
        if not alta:
            ax.add_patch(Rectangle((8, 8), 30, 6, fc=GRIS, ec="none"))
            ax.add_patch(Rectangle((8, 22), 84, 30, fc=SUP, ec=TINTA2, lw=1))
            ax.plot([8, 92], [22, 52], color=TINTA2, lw=.8); ax.plot([8, 92], [52, 22], color=TINTA2, lw=.8)
            for i in range(3): ax.add_patch(Rectangle((8, 58 + i * 7), 70 - i * 15, 3.2, fc=GRIS, ec="none"))
            ax.add_patch(FancyBboxPatch((8, 82), 34, 9, boxstyle="round,pad=0,rounding_size=1", fc=SUP, ec=TINTA2, lw=1.2))
            ax.text(25, 86.5, "Botón", ha="center", va="center", fontsize=9, color=TINTA2)
            ax.set_title("Baja fidelidad: estructura", fontsize=11, color=TINTA)
        else:
            ax.text(8, 11, "Diseño de interacción", fontsize=12.5, fontweight="bold", color="#000e78", va="center")
            ax.add_patch(FancyBboxPatch((8, 22), 84, 30, boxstyle="round,pad=0,rounding_size=2", fc="#dbe8f8", ec="none"))
            ax.add_patch(Circle((50, 37), 8, fc="#2a78d6", ec="none", alpha=.6))
            ax.text(8, 60, "García, L. (2024)", fontsize=9.5, color=TINTA2, va="center")
            ax.text(8, 67, "Disponible · Sala 2, estantería 4", fontsize=9.5, color="#0b6b4a", va="center", fontweight="bold")
            ax.text(8, 74, "2.ª edición · 320 páginas", fontsize=9, color=TINTA2, va="center")
            ax.add_patch(FancyBboxPatch((8, 82), 34, 9, boxstyle="round,pad=0,rounding_size=1.5", fc="#000e78", ec="none"))
            ax.text(25, 86.5, "Reservar", ha="center", va="center", fontsize=9.5, color=SUP, fontweight="bold")
            ax.set_title("Alta fidelidad: tipografía, color, contenido real", fontsize=11, color=TINTA)
    fig.text(0.5, 0.01, "La estructura se conserva; cambian el aspecto, el contenido y el detalle de la interacción.", ha="center", fontsize=9.5, color=TINTA2)
    guardar(fig, "t3_transicion.svg")


def t6_iconos():
    fig, ax = plt.subplots(figsize=(9, 3.6)); ax.set_xlim(0, 15); ax.set_ylim(0, 6); ax.axis("off")
    def lupa(cx, cy, r):
        ax.add_patch(Circle((cx - r * .15, cy + r * .15), r * .55, fill=False, ec=TINTA, lw=max(1, r * 3)))
        ax.plot([cx + r * .25, cx + r * .65], [cy - r * .25, cy - r * .65], color=TINTA, lw=max(1, r * 3), solid_capstyle="round")
    tit = [("Solo icono", 1.6), ("Icono + etiqueta", 6.6), ("Solo etiqueta", 11.6)]
    for t, x in tit: ax.text(x + 1, 5.5, t, ha="center", fontsize=10.5, fontweight="bold", color=TINTA)
    for i, (x, et) in enumerate([(1.6, None), (6.6, "Buscar"), (11.6, "Buscar")]):
        caja(ax, x - 0.6, 3.2, 3.2, 1.6, None, fc=SUP, ec=TINTA2, lw=1.2, r=0.15)
        if i < 2: lupa(x + (0.4 if et else 1.0), 4.0, 0.55)
        if et: ax.text(x + (1.2 if i == 1 else 1.0), 4.0, et, va="center", ha="left" if i == 1 else "center", fontsize=11, color=TINTA)
    notas = ["Rápido de leer si el icono\nes universal; ambiguo si no", "La opción más clara:\nreconocible y sin ambigüedad", "Claro, pero ocupa más\ny se escanea peor"]
    for (t, x), n in zip(tit, notas): ax.text(x + 1, 2.2, n, ha="center", va="center", fontsize=9, color=TINTA2)
    ax.text(7.5, 0.5, "Tamaños mínimos de toque: 24 × 24 px (WCAG 2.2, AA) y 44 × 44 pt recomendados (Apple).", ha="center", fontsize=9, color=TINTA2, style="italic")
    guardar(fig, "t6_iconos.svg")


def t7_gestalt():
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.2))
    for ax in axs: ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    for i in range(4):
        for j in range(4):
            axs[0].add_patch(Circle((1.5 + j * 1.1 + (2.5 if j >= 2 else 0), 2 + i * 1.8), .38, fc=S[0]))
            axs[1].add_patch(Circle((1.5 + j * 2.2, 2 + i * 1.8), .38, fc=S[0] if i % 2 == 0 else S[1]))
    from matplotlib.patches import Arc, Wedge
    axs[2].add_patch(Arc((5, 5.5), 6, 6, theta1=20, theta2=340, lw=3, color=TINTA))
    axs[2].add_patch(Arc((5, 5.5), 6, 6, theta1=350, theta2=10, lw=0))
    xs = [x / 10 for x in range(10, 91)]
    import math as m
    axs[3].plot(xs, [5 + 2.5 * m.sin(x / 1.4) for x in xs], color=S[2], lw=3)
    axs[3].plot(xs, [5 - 2.5 * m.sin(x / 1.4) for x in xs], color=S[0], lw=3)
    for ax, t, d in zip(axs, ["Proximidad", "Semejanza", "Cierre", "Continuidad"],
                         ["Lo cercano se agrupa:\nvemos dos columnas", "Lo parecido se agrupa:\nvemos filas por color", "Completamos la forma:\nvemos un círculo", "Seguimos la curva:\nvemos dos líneas"]):
        ax.set_title(t, fontsize=11, color=TINTA, fontweight="bold")
        ax.text(5, -0.6, d, ha="center", va="top", fontsize=9, color=TINTA2)
    guardar(fig, "t7_gestalt.svg")


def t9_tokens():
    fig, ax = plt.subplots(figsize=(10, 3.8)); ax.set_xlim(0, 16); ax.set_ylim(0, 6); ax.axis("off")
    cols = [("Primitivos", ["azul-900: #000e78", "gris-50: #f6f6f4", "espacio-4: 16 px", "radio-2: 8 px"], S[0]),
            ("Semánticos", ["color-accion: azul-900", "color-fondo: gris-50", "espacio-componente: espacio-4", "radio-control: radio-2"], S[1]),
            ("De componente", ["boton-fondo: color-accion", "boton-relleno: espacio-componente", "boton-radio: radio-control", "tarjeta-fondo: color-fondo"], S[2])]
    for k, (t, items, c) in enumerate(cols):
        x = 0.2 + k * 5.4
        ax.text(x + 2.3, 5.55, t, ha="center", fontsize=11, fontweight="bold", color=TINTA)
        for i, it in enumerate(items):
            caja(ax, x, 4.3 - i * 1.15, 4.6, 0.9, it, fc=SUP, ec=c, lw=1.6, fs=8.5)
        if k < 2: flecha(ax, (x + 4.65, 2.6), (x + 5.35, 2.6))
    ax.text(8, -0.05, "Cambiar un primitivo (un azul) actualiza todos los componentes que lo usan: así escala un sistema de diseño.", ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "t9_tokens.svg")


def t11_especificacion():
    fig, ax = plt.subplots(figsize=(9, 4.6)); ax.set_xlim(0, 100); ax.set_ylim(60, 0); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(FancyBboxPatch((20, 8), 50, 40, boxstyle="round,pad=0,rounding_size=2", fc=SUP, ec="#c9cfe0", lw=1.4))
    ax.text(26, 16, "Renovar préstamo", fontsize=11, fontweight="bold", color=TINTA, va="center")
    ax.text(26, 24, "Diseño de interacción · vence 02/12", fontsize=8.5, color=TINTA2, va="center")
    ax.add_patch(FancyBboxPatch((26, 34), 24, 8, boxstyle="round,pad=0,rounding_size=1.2", fc="#000e78", ec="none"))
    ax.text(38, 38, "Renovar", ha="center", va="center", fontsize=9, color=SUP, fontweight="bold")
    rojo = "#c0392b"
    ax.annotate("", (20, 52), (70, 52), arrowprops=dict(arrowstyle="<->", color=rojo, lw=1)); ax.text(45, 55, "320 px", ha="center", fontsize=8.5, color=rojo)
    ax.annotate("", (20, 30), (26, 30), arrowprops=dict(arrowstyle="<->", color=rojo, lw=1)); ax.text(23, 28.3, "24", ha="center", fontsize=8, color=rojo)
    ax.annotate("", (52, 34), (52, 42), arrowprops=dict(arrowstyle="<->", color=rojo, lw=1)); ax.text(53.5, 38, "44 px", fontsize=8, color=rojo, va="center")
    notas = [(76, 16, "Título: 20/28 px, semibold,\ncolor-texto-principal"), (76, 30, "Botón: boton-primario,\nradio-control (8 px)"),
             (76, 44, "Estados: reposo, foco,\npulsado, cargando, error")]
    for x, y, t in notas:
        ax.text(x, y, t, fontsize=8.5, color=TINTA, va="center")
        ax.plot([x - 1, 71], [y, y], color=rojo, lw=.8, ls=":")
    guardar(fig, "t11_especificacion.svg")


def t1_decisiones():
    fig, ax = plt.subplots(figsize=(9, 3.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6.2)
    preg = ["¿Encuentran la función?", "¿Entienden el flujo?", "¿Se lee bien el texto?", "¿Transmite confianza la marca?", "¿Se percibe rápida la respuesta?"]
    vals = [(1, 1), (1, 1), (0, 1), (0, 1), (0, 1)]
    ax.text(5.6, 5.8, "Baja", ha="center", fontsize=10.5, fontweight="bold", color=TINTA); ax.text(7.8, 5.8, "Alta", ha="center", fontsize=10.5, fontweight="bold", color=TINTA)
    for i, (q, (b, a)) in enumerate(zip(preg, vals)):
        y = 4.9 - i * 1.0
        ax.add_patch(FancyBboxPatch((0.1, y - 0.42), 9.0, 0.84, boxstyle="round,pad=0,rounding_size=0.05", fc=CAJA if i % 2 == 0 else SUP, ec="none"))
        ax.text(0.3, y, q, va="center", fontsize=10, color=TINTA)
        for x, v in ((5.6, b), (7.8, a)):
            ax.text(x, y, "✓ la valida" if v else "✗ no la valida", ha="center", va="center", fontsize=9.5, color="#0f6b45" if v else "#a52a1a")
    guardar(fig, "t1_decisiones.svg")

if __name__ == "__main__":
    for f in (tema4, tema5, tema7, tema8, tema9, t1_decisiones, t3_transicion, t6_iconos, t7_gestalt, t9_tokens, t11_especificacion):
        f()
