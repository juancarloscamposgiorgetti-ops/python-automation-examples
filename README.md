# Generador automático de firmas de correo

Script en Python que genera firmas de correo corporativas automáticamente.

## Cómo funciona

1. Se carga un Excel con datos de empleados.
2. Se carga una carpeta con fotos de los empleados.
3. Se utiliza una plantilla de firma.
4. El script genera automáticamente una firma personalizada para cada empleado.

## Tecnologías

- Python
- Pillow
- Pandas

## Datos utilizados

Excel con columnas:

NOMBRE  
CARGO  
CORREO  
TELEFONO  
SUCURSAL  

Las fotos deben tener como nombre el código del empleado.

## Resultado

Se generan imágenes JPG con la firma personalizada para cada empleado.


# Generador Automático de Fichas Técnicas de Productos

Script en Python que genera automáticamente fichas técnicas de productos a partir de una plantilla de diseño, datos de un archivo Excel y las imágenes de los productos.

Este sistema permite crear cientos de fichas técnicas de forma automática, ahorrando muchas horas de trabajo manual en diseño.

---

## Funcionalidades

- Generación automática de fichas técnicas en imagen
- Lectura de datos desde archivo Excel
- Inserción automática de imagen del producto
- Inserción automática del logo del fabricante
- Ajuste automático del texto para evitar que se desborde
- Eliminación automática de fondo en imágenes de producto
- Generación masiva de fichas técnicas

---

## Tecnologías utilizadas

- Python
- Pillow (PIL)
- Pandas

---

## Estructura del proyecto

project/
│
├── basefichatecnica.jpeg # plantilla base de la ficha
├── basefichaexcel.xlsx # datos de productos
│
├── productosbase/ # imágenes de productos
│ ├── 000001.jpg
│ ├── 000002.jpg
│
├── fabricantebase/ # logos de fabricantes
│ ├── marca1.jpg
│ ├── marca2.jpg
│
├── generados/ # fichas técnicas generadas automáticamente
│
└── script.py # script principal

---

## Formato del Excel

El archivo Excel debe contener columnas como:

- SKU
- FABRICANTE
- NOMBRE
- NOMBRECOMERCIAL
- CATEGORIA
- SUBCATEGORIA
- PPA
- DescripcionComercial
- DescripcionTecnica
- DescripciondeUso

---

## Funcionamiento

1. El script carga una plantilla base de ficha técnica.
2. Lee los datos de productos desde un archivo Excel.
3. Inserta automáticamente:

   - imagen del producto
   - logo del fabricante
   - nombre comercial
   - información del producto
   - descripciones comerciales y técnicas

4. Ajusta automáticamente el tamaño del texto para que encaje en la ficha.
5. Genera una imagen final de la ficha técnica.

---

## Resultado

El sistema genera automáticamente una ficha técnica por cada producto del Excel.

Ejemplo:

