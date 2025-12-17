import re
import requests
import os # <--- Importación necesaria para crear carpetas

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# --- Directorio de destino ---
DIR_DESTINO = 'libros_gutenberg'

def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Gets the urls for books in the Gutenberg project with numbers `n`."""
    assert n == -1 or min(n) > 0, ( "n can only take values greater than zero "
                                    "or -1 if all links are desired" )
    # Get the html of the top books in Gutenberg project
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        response = requests.get(url)

        # Parse contents with BeautifulSoup
        parser = BeautifulSoup(response.text, 'html.parser')

        # Get links of books
        ordered_list = parser.find('ol')  # get first ordered list
        list_items = ordered_list.find_all('li')  # list items inside
        if(n != -1):
            # Asegurarse de que 'n' es iterable
            if isinstance(n, int):
                n = [n]
            list_filtered = [list_items[i-1] for i in list(n) if 0 < i <= len(list_items)]
        else:
            list_filtered = list_items

        prefix = "https://www.gutenberg.org"
        suffix = ".txt.utf-8"
        links, titles = [], []
        for li in list_filtered:
            # Asegurarse de que el elemento contiene un enlace
            anchor = li.find("a")
            if anchor and anchor.get("href"):
                links.append(prefix + anchor.get("href") + suffix)
                
                # replace whitespaces by underscores
                title = re.sub( r'\s+', '_', li.get_text())
                
                # remove numbers and parenthesis at end of filename
                title = re.sub(r'_\(\d+\)$', '', title)
                
                # Además, limpiar caracteres inválidos para nombres de archivo
                title = re.sub(r'[\\/:*?"<>|]', '', title)
                
                title += r'.txt'  # add file extension
                titles.append(title)
        return links, titles

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        return [], []

def download_file(url, name):
    # Une el directorio con el nombre del archivo
    full_path = os.path.join(DIR_DESTINO, name) 
    
    response = requests.get(url, stream=True)
    # Usa la ruta completa para abrir el archivo
    with open(full_path, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):  #10kb chunks
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links, names):
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, links, names)

def store_files_slow(links, names):
    for url, name in zip(links, names):
        download_file(url, name)

def main( n = -1 ):
    # --- LÍNEA AGREGADA: Crea la carpeta ---
    os.makedirs(DIR_DESTINO, exist_ok=True)
    print(f"Carpeta '{DIR_DESTINO}' creada/verificada.")
    
    links, titles = get_links(n)
    
    if not links:
        print("No se encontraron enlaces para descargar.")
        return

    store_files(links, titles)
    print("Done")

n = range(1, 100)
main( n )
