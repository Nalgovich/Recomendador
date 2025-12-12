import time
import os

try:
    import urllib.request
except:
    print("Error: urllib no disponible") 
    exit() 


os.makedirs('libros_gutenberg', exist_ok=True)

for book_id in range(1, 101):
    # This line is indented once, inside the 'for' loop.
    try:
        
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        response = urllib.request.urlopen(url, timeout=10)
        contenido = response.read().decode('utf-8')
        
        
        with open(f'libros_gutenberg/libro_{book_id}.txt', 'w', encoding='utf-8') as f:
            # This line is indented three times (inside 'for', 'try', AND 'with')
            f.write(contenido)
            
        print(f"Descargado: Libro {book_id}")
        time.sleep(1)
        
    
    except Exception as e:
        # This code is indented twice (inside 'for' AND inside 'except')
        print(f"Error libro {book_id}: {str(e)}")
