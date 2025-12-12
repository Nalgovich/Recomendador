import time
import os

try:
    import urllib.request # Indented under 'try'
except:
    print("Error: urllib no disponible") # Indented under 'except'
    exit() # Indented under 'except'

# This line is not inside a block, so it is at the root level.
os.makedirs('libros_gutenberg', exist_ok=True)

for book_id in range(1, 101):
    # This line is indented once, inside the 'for' loop.
    try:
        # All lines below are indented twice (inside 'for' AND inside 'try')
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        response = urllib.request.urlopen(url, timeout=10)
        contenido = response.read().decode('utf-8')
        
        # The 'with' statement is also inside the 'try'
        with open(f'libros_gutenberg/libro_{book_id}.txt', 'w', encoding='utf-8') as f:
            # This line is indented three times (inside 'for', 'try', AND 'with')
            f.write(contenido)
            
        print(f"Descargado: Libro {book_id}")
        time.sleep(1)
        
    # This 'except' is indented once (matching the inner 'try')
    except Exception as e:
        # This code is indented twice (inside 'for' AND inside 'except')
        print(f"Error libro {book_id}: {str(e)}")
