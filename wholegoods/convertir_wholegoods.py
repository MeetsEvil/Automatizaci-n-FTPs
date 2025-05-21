import os
import pandas as pd
import shutil
from collections import defaultdict
 
# Ruta de los archivos
ruta = r"C:\Users\ogarci02\Downloads\AutomatizadoFTP2\AutomatizadoFTP\wholegoods"
prefijos = ["CM212F", "CM216F", "FG795F"]
 
# === FUNCIONES DE PARSEO POR ARCHIVO ===
def dividir_linea_cm212f(linea):
    total_units_raw2 = linea[65:69].strip()
    total_units2 = total_units_raw2.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    total_weight_raw3 = linea[69:77].strip()
    total_weight3 = total_weight_raw3.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    total_weight_raw4 = linea[268:].strip()
    total_weight4 = total_weight_raw4.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    
 
    return {
        "Freight Type": linea[0:1].strip(),
        "Ship Number": linea[1:8].strip(),
        "Load Number": linea[8:16].strip(),
        "Carrier ID": linea[16:26].strip(),
        "Ship Date": linea[26:34].strip(),
        "Trailer No": linea[34:49].strip(),
        "Bill of Lading #": linea[49:56].strip(),
        "Warehouse": linea[56:59].strip(),
        "# of Stops": linea[59:62].strip(),
        "Drop Number": linea[62:65].strip(),
        "Total Units": total_units2,
        "Total Weight": total_weight3,
        "Ship to City": linea[77:112].strip(),
        "Ship to State": linea[112:114].strip(),
        "Ship to Zip": linea[114:124].strip(),
        "International": linea[124:129].strip(),
        "Transmission Date": linea[129:137].strip(),
        "Store Date/Time": linea[137:163].strip(),
        "Clave Destina": linea[163:198].strip(),
        "Ship to Address": linea[198:233].strip(),
        "Transportation": linea[233:268].strip(),
        "Shipment Gross Weight": total_weight4
    }
def quitar_ceros_item_qty(valor):
    # Elimina ceros a izquierda y derecha en cantidades enteras
    valor_limpio = valor.lstrip('0').rstrip('0')
    return valor_limpio if valor_limpio else '0'

def quitar_ceros_izquierda_con_punto(valor):
    try:
        numero = float(valor)
        if numero.is_integer():
            return str(int(numero))  # Quita decimales si son .000
        else:
            return str(numero)
    except ValueError:
        return valor.strip()
 
def dividir_linea_cm216f(linea):

    raw_price = linea[150:169].strip().rjust(19, '0')
    price_con_punto = quitar_ceros_izquierda_con_punto(raw_price[:11] + '.' + raw_price[11:])
 
    raw_cost = linea[169:188].strip().rjust(19, '0')
    cost_con_punto = quitar_ceros_izquierda_con_punto(raw_cost[:11] + '.' + raw_cost[11:])
 
    raw_value = linea[188:].strip().rjust(19, '0')
    value_con_punto = quitar_ceros_izquierda_con_punto(raw_value[:11] + '.' + raw_value[11:])
 
    # Pallet or Box
    pallet_or_box = linea[135:139].strip().lstrip('0') or '0'
    net = linea[139:147].strip().lstrip('0') or '0'
 
    return {
        "Shipment Number": linea[0:7].strip(),
        "Load Number": linea[7:15].strip(),
        "Vin Number": linea[15:40].strip(),
        "Model Number (producto)": linea[40:55].strip(),
        "Model Description": linea[55:85].strip(),
        "Work Order Number": linea[85:92].strip(),
        "Crate Serial #": linea[92:99].strip(),
        "Commodity Code": linea[99:104].strip(),
        "Container Type": linea[104:109].strip(),
        "TimeStamp": linea[109:135].strip(),
        "Pallet or Box Number": pallet_or_box,
        "Net Weight KG": net,
        "Country of Origin": linea[147:150].strip(),
        "Unit Item Price": price_con_punto,
        "Unit Material Cost": cost_con_punto,
        "Unit MX Value Add": value_con_punto
    }
 
def dividir_linea_fg795f(linea):
    raw_cantidad = linea[74:84].strip().rjust(10, '0')
    cantidad_con_punto = quitar_ceros_izquierda_con_punto(raw_cantidad[:7] + '.' + raw_cantidad[7:])
 
    return {
        "clave_producto": linea[0:15].strip(),
        "descripcion": linea[15:45].strip(),
        "factura": linea[45:52].strip(),
        "?????": linea[52:59].strip(),
        "clave_material": linea[59:74].strip(),
        "cantidad": cantidad_con_punto,
        "clave_unidad": linea[84:86].strip(),
        "Time Stamp": linea[86:].strip(),
    }
 
# === SELECCIÓN DE PARSER POR PREFIJO ===
def obtener_parser(prefijo):
    if prefijo == "CM212F":
        return dividir_linea_cm212f
    elif prefijo == "CM216F":
        return dividir_linea_cm216f
    elif prefijo == "FG795F":
        return dividir_linea_fg795f
    else:
        raise ValueError(f"No hay función de parseo definida para {prefijo}")
 
# === AGRUPAR ARCHIVOS POR FECHA ===
archivos = os.listdir(ruta)
fechas_archivos = defaultdict(list)
 
for archivo in archivos:
    for prefijo in prefijos:
        if archivo.startswith(prefijo):
            partes = archivo.split("_")
            if len(partes) > 1:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                fecha_completa = "_".join(partes[1:])  # e.g., 20250505_121530_123456
                fechas_archivos[fecha_completa].append(archivo)

# === CREAR CARPETAS Y MOVER ARCHIVOS ===
for fecha_valida in sorted(fechas_archivos.keys()):
    # Crear carpeta con el nombre de la fecha
    carpeta_fecha = os.path.join(ruta, fecha_valida)
    if not os.path.exists(carpeta_fecha):
        os.makedirs(carpeta_fecha)
 
    # Mover archivos a la carpeta correspondiente
    for archivo in fechas_archivos[fecha_valida]:
        ruta_completa = os.path.join(ruta, archivo)
        shutil.move(ruta_completa, os.path.join(carpeta_fecha, archivo))
 
    # === CARGAR Y PARSEAR LOS ARCHIVOS ===
    dataframes = {}
    for prefijo in prefijos:
        archivos_fecha = fechas_archivos[fecha_valida]
        archivo_nombre = next((a for a in archivos_fecha if a.startswith(prefijo)), None)
        if archivo_nombre:
            ruta_completa = os.path.join(carpeta_fecha, archivo_nombre)
            parser = obtener_parser(prefijo)
            with open(ruta_completa, 'r', encoding='latin1') as f:
                lineas = f.readlines()
            registros = [parser(linea) for linea in lineas if linea.strip()]
            df = pd.DataFrame(registros)
            dataframes[prefijo] = df
            print(f"Archivo {archivo_nombre} procesado con {len(df)} registros.")
 
    # === GUARDAR CADA ARCHIVO COMO EXCEL DENTRO DE LA CARPETA ===
    for prefijo in dataframes:
        archivo_nombre = next((a for a in fechas_archivos[fecha_valida] if a.startswith(prefijo)), None)
        if archivo_nombre:
            nombre_salida = os.path.splitext(archivo_nombre)[0] + ".xlsx"
            ruta_salida = os.path.join(carpeta_fecha, nombre_salida)
            dataframes[prefijo].to_excel(ruta_salida, index=False)
            print(f"Archivo Excel guardado: {ruta_salida}")
  