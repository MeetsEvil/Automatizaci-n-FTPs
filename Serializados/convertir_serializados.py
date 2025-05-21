import os
import pandas as pd
import shutil
from collections import defaultdict
 
# Ruta de los archivos
ruta = "Serializados"
prefijos = ["CM907F", "FG808F", "FG797F", "FG809F"]
 
# === FUNCIONES DE PARSEO POR ARCHIVO ===
def dividir_linea_cm907f(linea):
    total_units_raw = linea[212:216].strip()
    total_units = total_units_raw.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    total_units_raw2 = linea[216:224].strip()
    total_units2 = total_units_raw2.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    total_units_raw3 = linea[224:232].strip()
    total_units3 = total_units_raw3.lstrip('0') or '0'  # Quita ceros a la izquierda, pero deja "0" si es todo ceros
    
 
    return {
        "Ship Number/CIMS/load": linea[0:9].strip(),
        "Store Date/Time": linea[9:35].strip(),
        "Bill of Lading": linea[35:42].strip(),
        "Ship Date": linea[42:50].strip(),
        "Ship to Name": linea[50:85].strip(),
        "Ship to Address": linea[85:120].strip(),
        "Ship to City": linea[120:155].strip(),
        "Ship to State": linea[155:157].strip(),
        "Ship to Zip": linea[157:167].strip(),
        "Carrier ID": linea[167:177].strip(),
        "Transportation": linea[177:212].strip(),
        "Total Units": total_units,
        "Total Weight": total_units2,
        "Shipment Gross Weight": total_units3,
        "Create Date": linea[232:242].strip(),
        "Create Time": linea[242:250].strip(),
        "Create User": linea[250:260].strip(),
        "Create Program": linea[260:270].strip(),
        "Unknown Field": linea[270:].strip()
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
 
def dividir_linea_fg808f(linea):
    # Item Qty limpio sin punto, sin ceros izq/der
    raw_item = linea[61:71].strip()
    item_qty = quitar_ceros_item_qty(raw_item)
 
    # Prices
    raw_price = linea[134:153].strip().rjust(19, '0')
    price_con_punto = quitar_ceros_izquierda_con_punto(raw_price[:11] + '.' + raw_price[11:])
 
    raw_cost = linea[153:172].strip().rjust(19, '0')
    cost_con_punto = quitar_ceros_izquierda_con_punto(raw_cost[:11] + '.' + raw_cost[11:])
 
    raw_value = linea[172:].strip().rjust(19, '0')
    value_con_punto = quitar_ceros_izquierda_con_punto(raw_value[:11] + '.' + raw_value[11:])
 
    # Pallet or Box
    pallet_or_box = linea[130:134].strip().lstrip('0') or '0'
 
    return {
        "Item Number": linea[0:15].strip(),
        "Item Description": linea[15:45].strip(),
        "Manifest Number": linea[45:54].strip(),
        "Work Order": linea[54:61].strip(),
        "Item Qty": item_qty,
        "Item U of M": linea[71:73].strip(),
        "TimeStamp": linea[73:99].strip(),
        "Unknown Field": linea[99:108].strip(),
        "Shipment Number/BOL": linea[108:115].strip(),
        "Trailer No": linea[115:130].strip(),
        "Pallet or Box": pallet_or_box,
        "Unit Item Price": price_con_punto,
        "Unit Material Cost": cost_con_punto,
        "Unit MX Value Add": value_con_punto
    }
 
def dividir_linea_fg797f(linea):
    raw_cantidad = linea[76:86].strip().rjust(10, '0')
    cantidad_con_punto = quitar_ceros_izquierda_con_punto(raw_cantidad[:7] + '.' + raw_cantidad[7:])
 
    return {
        "clave_producto": linea[0:15].strip(),
        "descripcion": linea[15:45].strip(),
        "factura Manifiesto": linea[45:53].strip(),
        "????? Adicional3": linea[53:54].strip(),
        "?????": linea[54:61].strip(),
        "clave_material": linea[61:76].strip(),
        "cantidad": cantidad_con_punto,
        "clave_unidad": linea[86:88].strip(),
        "Time Stamp": linea[88:].strip(),
    }
 
def dividir_linea_fg809f(linea):
    raw_inter = linea[51:58].strip()
    inter = raw_inter.lstrip('0') or '0'
 
    return {
        "manfst": linea[0:9].strip(),
        "?": linea[9:16].strip(),
        "clave_producto": linea[16:31].strip(),
        "??": linea[31:51].strip(),
        "???": inter,
        "vin": linea[58:70].strip(),
        "****": linea[70:92].strip(),
        "????": linea[92:].strip()
    }
 
# === SELECCIÓN DE PARSER POR PREFIJO ===
def obtener_parser(prefijo):
    if prefijo == "CM907F":
        return dividir_linea_cm907f
    elif prefijo == "FG808F":
        return dividir_linea_fg808f
    elif prefijo == "FG797F":
        return dividir_linea_fg797f
    elif prefijo == "FG809F":
        return dividir_linea_fg809f
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
  