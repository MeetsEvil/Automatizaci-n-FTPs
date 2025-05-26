# Automatización de Procesamiento de Archivos FTP de Exportación
 
## Descripción general
 
Este proyecto fue desarrollado para automatizar la separación, procesamiento y generación de archivos de exportación para tres procesos específicos: **Serializados**, **No Serializados** y **Wholegoods**.
 
## Objetivo
 
- Reducir el tiempo y esfuerzo en la gestión de archivos FTP.
- Generar archivos `.txt` y `.xlsx` organizados y listos para uso operativo o revisión.
- Crear archivos Excel con información tabulada, limpia y lista para ser utilizada.
 
## Características principales
 
- Soporte para los procesos de **Serializados**, **No Serializados** y **Wholegoods**.
- Identificación automática de archivos por su fecha completa de creación (año, mes, día, minuto, segundo y microsegundo).
- Separación de archivos en carpetas por fecha.
- Procesamiento de datos para limpiar ceros a la izquierda y derecha, así como agregar punto decimal donde corresponde.
 
## Lógica del código
 
1. Agrupa los archivos por su fecha de creación completa.
2. Crea una carpeta con la fecha exacta de los FTP (ejemplo: `20250505_140020`).
3. Guarda dentro de la carpeta los archivos `.txt` y los archivos generados en Excel `.xlsx`.
4. En cada Excel:
   - Columnas autoajustadas en ancho.
   - Altura fija de fila: **14.5**
5. Los datos en las tablas son formateados para:
   - Insertar el punto decimal correctamente.
   - Eliminar ceros innecesarios (a la izquierda y a la derecha del punto).
   - Presentar la información limpia y estructurada.
 
## Requisitos y consideraciones para su ejecución
 
- **Editor recomendado:** Visual Studio Code.
- **Forma de ejecución:** Desde la terminal (usando el botón "Run" o comando manual).
 
![Correr archivo (1)](https://github.com/user-attachments/assets/2d48028b-3e1b-4882-b045-92754296156e)

 
- **Estructura de carpetas:** Los archivos FTP `.txt` deben estar en la **misma carpeta** que el script.
- **Importante:**  
  - Solo deben existir archivos `.txt` válidos en la carpeta.
  - Evita tener otros tipos de archivo, ya que el script puede fallar.
  - Se recomienda **vaciar la carpeta de entrada después de cada ejecución** para evitar duplicados o errores.
 
## Tecnologías utilizadas
 
Este proyecto está desarrollado en **Python 3.x** y usa las siguientes tecnologías:
 
### 1. Python 3.13.3
 
- **Función:** Lenguaje de programación principal del script.
- **Uso:** Lectura, procesamiento, manipulación de archivos, cadenas, fechas y generación de carpetas.
- **Instalación:**  
Descargar desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  Asegúrate de marcar **"Add Python to PATH"** durante la instalación.
 
### 2. os
 
- **Función:** Módulo estándar de Python.
- **Uso:** Interacción con el sistema operativo (crear carpetas, listar y mover archivos).
- **Instalación:** Incluido por defecto en Python.
 
### 3. shutil
 
- **Función:** Módulo estándar de Python.
- **Uso:** Copiado y movimiento de archivos.
- **Instalación:** Incluido por defecto en Python.
 
### 4. datetime
 
- **Función:** Módulo estándar de Python.
- **Uso:** Manejo de fechas para clasificar archivos por su fecha de creación.
- **Instalación:** Incluido por defecto en Python.
 
### 5. openpyxl
 
- **Función:** Biblioteca externa.
- **Uso:** Creación de archivos Excel (.xlsx), ajuste automático de columnas y altura de filas.
- **Instalación:** Ejecutar en la terminal:
```bash
pip install openpyxl
