import time
import os
import re
import urllib.request
import urllib.error

# --- FUNCIÓN PARA OBTENER LA LISTA DE LIBROS TOP 100 (Nueva) ---
def obtener_libros_top_100():
    """Descarga la página de top 100 y extrae una lista de tuplas (titulo, book_id)."""
    url_top = "https://www.gutenberg.org/browse/scores/top"
    libros = []
    
    print(f"Buscando los 100 libros más descargados en: {url_top}")
    
    try:
        response = urllib.request.urlopen(url_top, timeout=15)
        html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error al descargar la lista de Top 100: {e}")
        return []

    # Patrón RegEx para encontrar los enlaces a los libros.
    # El patrón busca la estructura: <a href="/ebooks/ID">Título del Libro</a>
    # El Project Gutenberg usa la clase 'score' para la lista.
    # Usaremos un patrón que busca enlaces a '/ebooks/ID'
    
    # Patrón más específico para extraer ID y Título del enlace HTML:
    # re.DOTALL: Permite que '.' coincida con saltos de línea.
    # re.IGNORECASE: Ignora mayúsculas/minúsculas.
    patron = re.compile(
        r'<a href="/ebooks/(\d+)" title=".*?">(.+?)</a>', 
        re.DOTALL | re.IGNORECASE
    )
    
    # Usamos findall para obtener todas las coincidencias
    coincidencias = patron.findall(html_content)
    
    # El Project Gutenberg tiene enlaces duplicados y otros enlaces en la página.
    # Solo queremos los primeros 100 únicos, que son los de la lista principal.
    
    ids_vistos = set()
    for book_id, titulo_html in coincidencias:
        if book_id not in ids_vistos:
            # Reemplazar entidades HTML comunes si es necesario (ej. &amp; -> &)
            titulo_limpio = titulo_html.replace('&amp;', '&').strip()
            libros.append((titulo_limpio, book_id))
            ids_vistos.add(book_id)
            
            if len(libros) >= 100:
                break

    print(f"✅ Encontrados {len(libros)} libros para descargar.")
    return libros

# --- FUNCIÓN DE LIMPIEZA ---
def limpiar_titulo_para_archivo(titulo):
    """Limpia el título para que sea un nombre de archivo seguro."""
    # Elimina caracteres que son inválidos en nombres de archivo
    titulo_limpio = re.sub(r'[\\/:*?"<>|]', '_', titulo)
    # Normaliza espacios y guiones
    titulo_limpio = re.sub(r'\s+|-+', ' ', titulo_limpio).strip()
    # Limita la longitud para evitar problemas en el sistema de archivos
    if len(titulo_limpio) > 100:
        titulo_limpio = titulo_limpio[:100].rstrip() + '...'
        
    return titulo_limpio

# --- LÓGICA PRINCIPAL DE DESCARGA ---

# 1. Obtener la lista de los top 100 libros
libros_a_descargar = obtener_libros_top_100()

if not libros_a_descargar:
    print("No se pudo obtener la lista de libros top 100. Saliendo del script.")
    exit()

os.makedirs('libros_gutenberg', exist_ok=True)
print("\nIniciando descarga de los libros...\n")

for i, (titulo, book_id) in enumerate(libros_a_descargar, start=1):
    try:
        # 2. Generar la URL de descarga del archivo .txt usando el ID
        # Nota: Usamos el ID para obtener el archivo .txt, no hay otra forma fiable.
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        
        response = urllib.request.urlopen(url, timeout=10)
        contenido = response.read().decode('utf-8')
        
        # 3. Limpiar y usar el título extraído del hipervínculo
        nombre_archivo_limpio = limpiar_titulo_para_archivo(titulo)
        nombre_completo = f'libros_gutenberg/{nombre_archivo_limpio}.txt'
        
        with open(nombre_completo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"[{i:03d}/100] ✅ Descargado (ID {book_id}): {nombre_archivo_limpio}.txt")

        time.sleep(1) # Espera de 1 segundo para no saturar el servidor
        
    except urllib.error.HTTPError as http_e:
        if http_e.code == 404:
             print(f"[{i:03d}/100] ❌ Error libro {book_id}: No se encontró el archivo (404).")
        else:
             print(f"[{i:03d}/100] ❌ Error libro {book_id}: {str(http_e)}")
    except Exception as e:
        print(f"[{i:03d}/100] ❌ Error libro {book_id}: {str(e)}")

print("\nProceso de descarga finalizado.")
