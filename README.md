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
