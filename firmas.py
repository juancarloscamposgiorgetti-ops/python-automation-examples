from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

# =========================
# CONFIGURACIONES
# =========================
excel_file = "C:/jc_firma/colab2.xlsx"
plantilla_file = "C:/jc_firma/firma_vacia.png"
carpeta_salida = "C:/jc_firma/jpg/"
fuente_file = "C:/Users/jcampos/Desktop/jc 2/JC/Onest/static/Onest-Bold.ttf"
fuente_file2 = "C:/Users/jcampos/Desktop/jc 2/JC/Onest/static/Onest-Regular.ttf"
logo_file = "C:/jc_firma/logo_union2.png"  # Ruta del logo

os.makedirs(carpeta_salida, exist_ok=True)

# =========================
# CARGA DE DATOS
# =========================
df = pd.read_excel(excel_file)
plantilla_base = Image.open(plantilla_file)

# Fuentes
fuente_nombre   = ImageFont.truetype(fuente_file, 95)  # Nombre grande
fuente_cargo    = ImageFont.truetype(fuente_file, 54)   # Cargo
fuente_texto    = ImageFont.truetype(fuente_file2, 55)   # Correo y teléfono
fuente_sucursal = ImageFont.truetype(fuente_file, 35)   # Sucursal pequeña

# Cargar el logo
logo = Image.open(logo_file).resize((500, 600))  # Ajustar tamaño del logo

# =========================
# GENERACIÓN DE FIRMAS
# =========================
for i, row in df.iterrows():
    firma = plantilla_base.copy()
    draw = ImageDraw.Draw(firma)

    nombre   = str(row["NOMBRE1"]) if "NOMBRE1" in df.columns else ""
    cargo    = str(row["CARGO"]) if "CARGO" in df.columns else ""
    telefono = str(int(row["TELEFONO"])) if "TELEFONO" in df.columns and not pd.isna(row["TELEFONO"]) else ""
    correo   = str(row["CORREO"]) if "CORREO" in df.columns else ""
    sucursal = "SUCURSAL: " + str(row["SUCURSAL"]).upper() if "SUCURSAL" in df.columns else ""  # en mayúsculas

    # =========================
    # INSERTAR LOGO EN LA FIRMA
    # =========================
    firma.paste(logo, (135, 90), logo.convert("RGBA").split()[3])

    # =========================
    # TEXTOS
    # =========================
    # Nombre
    draw.text((785, 120), nombre, font=fuente_nombre, fill=(227, 10, 19))

    # Cargo
    draw.text((790, 235), cargo, font=fuente_cargo, fill=(235, 50, 60))

    # Sucursal pequeño alineado a la derecha, en la misma línea que el cargo
    if sucursal:
        draw.text((1880, 320), sucursal, font=fuente_sucursal, fill=(227, 10, 19))

    # Correo en blanco y más "negrita" (simulada)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            draw.text((830 + dx, 397 + dy), correo, font=fuente_texto, fill=(255, 255, 255))

    # Teléfono en blanco y más "negrita" (simulada)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            draw.text((830 + dx, 463 + dy), telefono, font=fuente_texto, fill=(255, 255, 255))

    # =========================
    # GUARDAR RESULTADO
    # =========================
    salida_path = os.path.join(carpeta_salida, f"{nombre}_firma.jpg")
    firma.save(salida_path)
    print(f"✅ Firma generada: {salida_path}")

print("\n🎉 Todas las firmas han sido generadas correctamente.")
