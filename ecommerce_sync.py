import pandas as pd
import os
from datetime import datetime


# Columnas estándar del catálogo de productos ecommerce
COLUMNAS = [
    "SKU",
    "NOMBRE",
    "CATEGORIA",
    "SUBCATEGORIA",
    "PRECIO",
    "STOCK",
    "FABRICANTE",
    "DESCRIPCION",
    "ACTIVO",
]

# Columna que identifica de forma única a cada producto
CLAVE_PRIMARIA = "SKU"

# Columna usada para resolver conflictos entre fuentes (fuente con valor mayor tiene prioridad)
COLUMNA_PRIORIDAD = "PRECIO"


def cargar_catalogo(ruta: str) -> pd.DataFrame:
    """Carga un catálogo de productos desde un archivo Excel.

    Args:
        ruta: Ruta al archivo Excel (.xlsx).

    Returns:
        DataFrame con los datos del catálogo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo no contiene la columna clave primaria.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    df = pd.read_excel(ruta)

    if CLAVE_PRIMARIA not in df.columns:
        raise ValueError(
            f"El archivo '{ruta}' debe contener la columna '{CLAVE_PRIMARIA}'."
        )

    # Normalizar SKU como texto sin espacios
    df[CLAVE_PRIMARIA] = df[CLAVE_PRIMARIA].astype(str).str.strip()

    return df


def union_catalogos(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
    """Realiza un UNION de dos catálogos de productos.

    Combina todos los productos de ambas fuentes. Cuando un SKU existe
    en ambas fuentes, se resuelve el conflicto conservando el registro
    de la fuente con mayor valor en COLUMNA_PRIORIDAD.

    Args:
        df_a: DataFrame con el catálogo de la fuente A.
        df_b: DataFrame con el catálogo de la fuente B.

    Returns:
        DataFrame unificado sin duplicados por SKU.
    """
    # Etiquetar cada fuente para resolver conflictos luego
    df_a = df_a.copy()
    df_b = df_b.copy()
    df_a["_fuente"] = "A"
    df_b["_fuente"] = "B"

    # UNION: concatenar ambas fuentes
    df_union = pd.concat([df_a, df_b], ignore_index=True)

    if COLUMNA_PRIORIDAD in df_union.columns:
        # Convertir a numérico; los valores no numéricos se reemplazan por 0
        # para que los registros con precio válido siempre tengan prioridad.
        df_union[COLUMNA_PRIORIDAD] = (
            pd.to_numeric(df_union[COLUMNA_PRIORIDAD], errors="coerce").fillna(0)
        )
        # Ordenar por prioridad descendente para que keep='first' conserve el mejor registro
        df_union = df_union.sort_values(
            by=[CLAVE_PRIMARIA, COLUMNA_PRIORIDAD], ascending=[True, False]
        )
    else:
        # Sin columna de prioridad, ordenar solo por SKU y fuente para resultado determinista.
        # En caso de SKU duplicado se conserva el registro de la fuente A (aparece primero).
        df_union = df_union.sort_values(by=[CLAVE_PRIMARIA, "_fuente"])

    # Eliminar duplicados por SKU, conservando el registro con mayor prioridad
    df_resultado = df_union.drop_duplicates(subset=[CLAVE_PRIMARIA], keep="first")

    # Eliminar columna auxiliar de fuente
    df_resultado = df_resultado.drop(columns=["_fuente"])

    return df_resultado.reset_index(drop=True)


def sincronizar(ruta_fuente_a: str, ruta_fuente_b: str, ruta_salida: str) -> None:
    """Sincroniza dos catálogos de ecommerce y exporta el resultado unificado.

    Lee los catálogos de las dos fuentes, realiza el UNION de productos,
    y guarda el catálogo sincronizado en un nuevo archivo Excel.

    Args:
        ruta_fuente_a: Ruta al Excel de la fuente A.
        ruta_fuente_b: Ruta al Excel de la fuente B.
        ruta_salida: Ruta del Excel de salida con el catálogo unificado.
    """
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Iniciando sincronización...")

    print(f"  Cargando fuente A: {ruta_fuente_a}")
    df_a = cargar_catalogo(ruta_fuente_a)
    print(f"    → {len(df_a)} productos encontrados en fuente A.")

    print(f"  Cargando fuente B: {ruta_fuente_b}")
    df_b = cargar_catalogo(ruta_fuente_b)
    print(f"    → {len(df_b)} productos encontrados en fuente B.")

    print("  Realizando UNION de catálogos...")
    df_sincronizado = union_catalogos(df_a, df_b)

    skus_solo_a = set(df_a[CLAVE_PRIMARIA]) - set(df_b[CLAVE_PRIMARIA])
    skus_solo_b = set(df_b[CLAVE_PRIMARIA]) - set(df_a[CLAVE_PRIMARIA])
    skus_comunes = set(df_a[CLAVE_PRIMARIA]) & set(df_b[CLAVE_PRIMARIA])

    print(f"    → Productos solo en fuente A:    {len(skus_solo_a)}")
    print(f"    → Productos solo en fuente B:    {len(skus_solo_b)}")
    print(f"    → Productos en ambas fuentes:    {len(skus_comunes)}")
    print(f"    → Total productos sincronizados: {len(df_sincronizado)}")

    # Crear directorio de salida si no existe
    directorio_salida = os.path.dirname(ruta_salida)
    if directorio_salida:
        os.makedirs(directorio_salida, exist_ok=True)

    df_sincronizado.to_excel(ruta_salida, index=False)
    print(f"  Catálogo sincronizado guardado en: {ruta_salida}")
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Sincronización completada.")


if __name__ == "__main__":
    # Rutas de los archivos de entrada y salida
    FUENTE_A = "catalogo_fuente_a.xlsx"
    FUENTE_B = "catalogo_fuente_b.xlsx"
    SALIDA = "catalogo_sincronizado.xlsx"

    sincronizar(FUENTE_A, FUENTE_B, SALIDA)
