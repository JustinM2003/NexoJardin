#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import shutil

def convert_utf16_to_utf8(input_file, output_file):
    """
    Convierte un archivo de UTF-16 a UTF-8
    """
    try:
        # Intentar UTF-16 primero
        try:
            with open(input_file, 'r', encoding='utf-16') as f:
                content = f.read()
            print(f"Archivo {input_file} leído como UTF-16")
        except UnicodeError:
            # Si no es UTF-16, probar UTF-8
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Archivo {input_file} ya está en UTF-8")
        
        # Verificar que es JSON válido
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error de JSON en {input_file}: {e}")
            return False
        
        # Escribir como UTF-8
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Archivo convertido guardado como: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error procesando {input_file}: {e}")
        return False

def main():
    files_to_convert = ['datos.json', 'usuarios.json']
    
    for filename in files_to_convert:
        print(f"\nProcesando {filename}...")
        output_filename = f"{filename.split('.')[0]}_utf8.json"
        
        if convert_utf16_to_utf8(filename, output_filename):
            print(f"✓ {filename} convertido exitosamente")
        else:
            print(f"✗ Error convirtiendo {filename}")
            return 1
    
    print("\n=== Proceso completado ===")
    print("Archivos convertidos:")
    print("- datos_utf8.json")
    print("- usuarios_utf8.json")
    print("\nAhora actualiza build.sh para usar estos archivos.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
