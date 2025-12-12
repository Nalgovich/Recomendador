import time
import os

try:
    import urllib.request
except:
    print("Error: urllib no disponible") 
    exit() 


os.makedirs('libros_gutenberg', exist_ok=True)

for book_id in range(1, 101):
    
    try:
        
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        response = urllib.request.urlopen(url, timeout=10)
        contenido = response.read().decode('utf-8')
        
        
        with open(f'libros_gutenberg/libro_{book_id}.txt', 'w', encoding='utf-8') as f:
            f.write(contenido)
            
        print(f"Descargado: Libro {book_id}")
        time.sleep(1)
    
    except Exception as e:
        print(f"Error libro {book_id}: {str(e)}")
