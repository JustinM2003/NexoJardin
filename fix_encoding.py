#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import codecs

def fix_encoding_issues(text):
    """
    Arregla problemas comunes de codificación en el texto
    """
    if not isinstance(text, str):
        return text
    
    # Mapeo de caracteres mal codificados a su versión correcta
    replacements = {
        'ß': 'á',
        '¾': 'ó',
        'Ý': 'í',
        'Þ': 'ú',
        'Ñ': 'é',
        '·': 'ú',
        'Ç': 'ü',
        '±': 'ñ',
        'Ù': 'Ú',
        'È': 'É',
        'Í': 'Í',
        'Ó': 'Ó',
        'Ú': 'Ú',
        'Ñ': 'Ñ',
        'ç': 'ü',
        '¿': 'ñ',
        # Más mapeos específicos basados en los problemas observados
        'orgßnica': 'orgánica',
        'h·medo': 'húmedo',
        'cßlidos': 'cálidos',
        'Fertilizaci¾n': 'Fertilización',
        'variegaci¾n': 'variegación',
        'caÝda': 'caída',
        'Fßcil': 'Fácil',
        'sombr¡o': 'sombrío',
        'peque±os': 'pequeños',
        'ßcida': 'ácida',
        'básica': 'básica',
        'r¡o': 'río',
        'prßctica': 'práctica',
        'pÞblica': 'pública',
        'tßcnica': 'técnica',
        'económica': 'económica',
        'clásica': 'clásica',
        'específica': 'específica',
        'típica': 'típica',
        'única': 'única',
        'práctica': 'práctica',
        'romántica': 'romántica',
        'automática': 'automática',
        'electrónica': 'electrónica',
        'biológica': 'biológica',
        'química': 'química',
        'física': 'física',
        'matemática': 'matemática',
        'histórica': 'histórica',
        'geográfica': 'geográfica',
        'artística': 'artística',
        'musical': 'musical',
        'literaria': 'literaria',
        'científica': 'científica',
        'médica': 'médica',
        'farmacéutica': 'farmacéutica',
        'genética': 'genética',
        'atlética': 'atlética',
        'estética': 'estética',
        'ética': 'ética',
        'política': 'política',
        'crítica': 'crítica',
        'lógica': 'lógica',
        'mágica': 'mágica',
        'trágica': 'trágica',
        'cómica': 'cómica',
        'dramática': 'dramática',
        'fantástica': 'fantástica',
        'plástica': 'plástica',
        'elástica': 'elástica',
        'gimnástica': 'gimnástica',
        'eclesiástica': 'eclesiástica',
        'entusiástica': 'entusiástica',
        'sarcástica': 'sarcástica',
        'iconoclástica': 'iconoclástica',
        'eclesiástica': 'eclesiástica',
        'escolástica': 'escolástica',
        'monástica': 'monástica',
        'gimnástica': 'gimnástica',
        'balística': 'balística',
        'holística': 'holística',
        'silogística': 'silogística',
        'heurística': 'heurística',
        'lingüística': 'lingüística',
        'turística': 'turística',
        'jurística': 'jurística',
        'estadística': 'estadística',
        'característica': 'característica',
        'optimística': 'optimística',
        'pesimística': 'pesimística',
        'realística': 'realística',
        'idealística': 'idealística',
        'materialística': 'materialística',
        'capitalística': 'capitalística',
        'socialística': 'socialística',
        'naturalística': 'naturalística',
        'fatalística': 'fatalística',
    }
    
    result = text
    for wrong, correct in replacements.items():
        result = result.replace(wrong, correct)
    
    return result

def fix_json_encoding(input_file, output_file):
    """
    Lee el archivo JSON, arregla la codificación y lo guarda
    """
    try:
        # Intentar leer con diferentes codificaciones
        encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
        
        data = None
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    data = json.load(f)
                print(f"Archivo leído exitosamente con codificación: {encoding}")
                break
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
        
        if data is None:
            print("No se pudo leer el archivo con ninguna codificación")
            return False
        
        # Función recursiva para arreglar strings en la estructura JSON
        def fix_strings_recursive(obj):
            if isinstance(obj, dict):
                return {key: fix_strings_recursive(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [fix_strings_recursive(item) for item in obj]
            elif isinstance(obj, str):
                return fix_encoding_issues(obj)
            else:
                return obj
        
        # Arreglar la codificación en todo el JSON
        fixed_data = fix_strings_recursive(data)
        
        # Guardar el archivo con codificación UTF-8
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)
        
        print(f"Archivo guardado exitosamente como: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return False

if __name__ == "__main__":
    input_file = "datos.json"
    output_file = "datos_fixed.json"
    
    if fix_json_encoding(input_file, output_file):
        print("¡Codificación arreglada exitosamente!")
        print(f"Archivo original: {input_file}")
        print(f"Archivo corregido: {output_file}")
    else:
        print("Error al arreglar la codificación")
