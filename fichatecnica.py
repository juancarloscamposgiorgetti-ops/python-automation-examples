from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

# =========================
# CONFIGURACIÓN
# =========================
BASE_DIR = "D:/emiliano/productofichatecnica/"

PLANTILLA = os.path.join(BASE_DIR, "basefichatecnica.jpeg")
EXCEL = os.path.join(BASE_DIR, "basefichaexcel.xlsx")

CARPETA_PRODUCTOS = os.path.join(BASE_DIR, "productosbase")
CARPETA_FABRICANTES = os.path.join(BASE_DIR, "fabricantebase")
CARPETA_SALIDA = os.path.join(BASE_DIR, "generados")

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# =========================
# CARGA
# =========================
df = pd.read_excel(EXCEL)
plantilla_base = Image.open(PLANTILLA).convert("RGB")

# =========================
# FUENTES
# =========================
FUENTE_PATH = "C:/Windows/Fonts/arialbd.ttf"
TAMANO_TITULO = 32
TAMANO_TEXTO = 28

font_titulo = ImageFont.truetype(FUENTE_PATH, TAMANO_TITULO)
font_texto = ImageFont.truetype(FUENTE_PATH, TAMANO_TEXTO)

# =========================
# FUNCIÓN AJUSTE DE TEXTO
# =========================
def dividir_texto(draw, texto, fuente, max_ancho):
    palabras = texto.split()
    lineas = []
    linea = ""
    for palabra in palabras:
        prueba = linea + palabra + " "
        w = draw.textbbox((0, 0), prueba, font=fuente)[2]
        if w <= max_ancho:
            linea = prueba
        else:
            lineas.append(linea.strip())
            linea = palabra + " "
    if linea:
        lineas.append(linea.strip())
    return lineas

# =========================
# FUNCIÓN QUITAR FONDO CREMA
# =========================
def quitar_fondo_por_bordes(img, tolerancia=45):
    img = img.convert("RGBA")
    pix = img.load()

    esquinas = [
        pix[0, 0],
        pix[img.width - 1, 0],
        pix[0, img.height - 1],
        pix[img.width - 1, img.height - 1]
    ]

    r_bg = sum(p[0] for p in esquinas) // 4
    g_bg = sum(p[1] for p in esquinas) // 4
    b_bg = sum(p[2] for p in esquinas) // 4

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pix[x, y]
            if (
                abs(r - r_bg) < tolerancia and
                abs(g - g_bg) < tolerancia and
                abs(b - b_bg) < tolerancia
            ):
                pix[x, y] = (r, g, b, 0)

    return img

# =========================
# POSICIONES Y MEDIDAS
# =========================
POS_PRODUCTO = (90, 220)
POS_FABRICANTE = (30, 40)

ANCHO_FABRICANTE = 220
ALTO_FABRICANTE = 120

POS_TEXTO_X = POS_PRODUCTO[0] + 460
POS_NOMBRE_Y = POS_PRODUCTO[1]

LINE_HEIGHT = 42
ESPACIO_ENTRE_CAMPOS = 8
MAX_ANCHO_TEXTO = 700

MARGEN_INFERIOR = 40
MAX_ANCHO_DESC = 1050

# =========================
# GENERACIÓN DE FICHAS
# =========================
for _, row in df.iterrows():
    ficha = plantilla_base.copy()
    draw = ImageDraw.Draw(ficha)

    sku = f"{int(row['SKU']):06d}"

    fabricante = str(row["FABRICANTE"])
    nombre = str(row.get("NOMBRE", "")).upper()
    nombrecomercial = str(row.get("NOMBRECOMERCIAL", "")).upper()
    categoria = str(row.get("CATEGORIA", "")).upper()
    subcategoria = str(row.get("SUBCATEGORIA", "")).upper()
    ppa = str(row.get("PPA", ""))

    descripcion_comercial = str(row.get("DescripcionComercial", ""))
    descripcion_tecnica = str(row.get("DescripcionTecnica", ""))
    descripcion_uso = str(row.get("DescripciondeUso", ""))

    # =========================
    # IMAGEN PRODUCTO
    # =========================
    producto_path = os.path.join(CARPETA_PRODUCTOS, f"{sku}.jpg")

    if os.path.exists(producto_path):
        producto = Image.open(producto_path)
        producto = quitar_fondo_por_bordes(producto, tolerancia=45)
        producto = producto.resize((450, 450), Image.LANCZOS)
        ficha.paste(producto, POS_PRODUCTO, producto)
    else:
        print(f"⚠️ No se encontró imagen del producto: {sku}")

    # =========================
    # IMAGEN FABRICANTE
    # =========================
    fab_path = os.path.join(CARPETA_FABRICANTES, f"{fabricante}.jpg")
    if os.path.exists(fab_path):
        fab = Image.open(fab_path).convert("RGBA")
        fab = fab.resize((ANCHO_FABRICANTE, ALTO_FABRICANTE), Image.LANCZOS)
        ficha.paste(fab, POS_FABRICANTE, fab)
    else:
        print(f"⚠️ No se encontró imagen de fabricante: {fabricante}")

    # =========================
    # NOMBRE COMERCIAL
    # =========================
    w, h = draw.textbbox((0, 0), nombrecomercial, font=font_titulo)[2:4]
    x_texto = POS_FABRICANTE[0] + ANCHO_FABRICANTE + 120
    y_texto = POS_FABRICANTE[1] + ALTO_FABRICANTE // 2 - h // 2 + 50
    draw.text((x_texto, y_texto), nombrecomercial, font=font_titulo, fill=(0, 0, 0))

    # =========================
    # TEXTO A LA DERECHA
    # =========================
    y_actual = POS_NOMBRE_Y
    for texto in [nombre, f"SKU: {sku}", categoria, subcategoria, ppa]:
        for linea in dividir_texto(draw, texto, font_titulo, MAX_ANCHO_TEXTO):
            draw.text((POS_TEXTO_X, y_actual), linea, font=font_titulo, fill=(0, 0, 0))
            y_actual += LINE_HEIGHT
        y_actual += ESPACIO_ENTRE_CAMPOS

    # =========================
    # DESCRIPCIONES INFERIORES
    # =========================
    y_inicio = POS_PRODUCTO[1] + 470
    espacio = ficha.height - y_inicio - MARGEN_INFERIOR

    textos = [descripcion_comercial, descripcion_tecnica, descripcion_uso]
    lineas = []

    for t in textos:
        for l in t.split("\n"):
            lineas.extend(dividir_texto(draw, l, font_texto, MAX_ANCHO_DESC))
        lineas.append("")

    tam = TAMANO_TEXTO
    while tam > 10:
        font_desc = ImageFont.truetype(FUENTE_PATH, tam)
        if len(lineas) * (tam + 2) <= espacio:
            break
        tam -= 1

    y = y_inicio
    for l in lineas:
        draw.text((POS_PRODUCTO[0], y), l, font=font_desc, fill=(0, 0, 0))
        y += tam + 2

    # =========================
    # GUARDAR
    # =========================
    salida = os.path.join(CARPETA_SALIDA, f"{sku}.jpg")
    ficha.save(salida, quality=95)
    print(f"✅ Generado: {salida}")

print("\n🎉 Todas las fichas técnicas fueron generadas.")
