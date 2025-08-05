#!/usr/bin/env python3
"""
Script para actualizar datos.json con los nuevos campos del modelo Producto
"""
import json
import sys

def fix_datos_json():
    # Leer el archivo actual
    with open('datos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Actualizar cada producto
    for item in data:
        if item['model'] == 'products.producto':
            fields = item['fields']
            
            # Si tiene el campo 'precio' (estructura antigua), actualizarlo
            if 'precio' in fields:
                precio_actual = float(fields['precio'])
                
                # Usar el precio actual como precio_base
                fields['precio_base'] = precio_actual
                
                # Valores por defecto para nuevos campos
                fields['porcentaje_extra'] = 0.0
                fields['incluir_iva'] = False
                fields['descripcion_corta'] = ""
                fields['medidas'] = ""
                
                # Mantener el precio actual calculado
                # (precio_base * (1 + porcentaje_extra/100) * (1.19 si incluir_iva else 1))
                fields['precio'] = precio_actual
            
            # Asegurar que todos los campos nuevos estén presentes
            if 'precio_base' not in fields:
                fields['precio_base'] = float(fields.get('precio', 0))
            if 'porcentaje_extra' not in fields:
                fields['porcentaje_extra'] = 0.0
            if 'incluir_iva' not in fields:
                fields['incluir_iva'] = False
            if 'descripcion_corta' not in fields:
                fields['descripcion_corta'] = ""
            if 'medidas' not in fields:
                fields['medidas'] = ""
    
    # Escribir el archivo actualizado
    with open('datos_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ': '))
    
    print("Archivo datos_fixed.json creado con éxito")
    print("Reemplaza el contenido de datos.json con el contenido de datos_fixed.json")

if __name__ == "__main__":
    fix_datos_json()
