#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def fix_encoding_issues(text):
    """
    Corrige problemas comunes de codificación en el texto
    """
    # Mapeo de caracteres problemáticos a sus equivalentes correctos
    replacements = {
        'β': 'á',  # á mal codificado
        '¾': 'ó',  # ó mal codificado
        '±': 'ñ',  # ñ mal codificado
        'Ý': 'í',  # í mal codificado
        'Ú': 'é',  # é mal codificado
        'Ø': 'ü',  # ü mal codificado
        '·': 'ú',  # ú mal codificado
        'ß': 'á',  # á alternativo
        '░': '°',  # símbolo de grados
        'µ': 'ú',  # ú alternativo
        'ý': 'í',  # í alternativo
        'Ñ': 'É',  # É mal codificado
        'ý': 'í',  # í alternativo
    }
    
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    
    return text

def fix_json_file(input_file, output_file):
    """
    Lee un archivo JSON con problemas de codificación y crea una versión corregida
    """
    try:
        # Intentar leer con diferentes codificaciones, incluyendo UTF-16
        content = None
        encodings = ['utf-16', 'utf-16-le', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Archivo leído exitosamente con codificación: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("No se pudo leer el archivo con ninguna codificación estándar")
            return False
        
        # Corregir problemas de codificación
        content = fix_encoding_issues(content)
        
        # Validar que sea JSON válido
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error de JSON después de la corrección: {e}")
            return False
        
        # Escribir el archivo corregido
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Archivo corregido guardado como: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return False

def main():
    # Corregir datos.json
    print("Corrigiendo datos.json...")
    if fix_json_file('datos.json', 'datos_fixed.json'):
        print("datos.json corregido exitosamente")
    else:
        print("Error corrigiendo datos.json")
        return 1
    
    # Corregir usuarios.json
    print("\nCorrigiendo usuarios.json...")
    if fix_json_file('usuarios.json', 'usuarios_fixed.json'):
        print("usuarios.json corregido exitosamente")
    else:
        print("Error corrigiendo usuarios.json")
        return 1
    
    print("\nProceso completado. Usa los archivos *_fixed.json para deployment.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
