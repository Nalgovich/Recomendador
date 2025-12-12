import sys
import os

def resumir(archivo):
    ruta = os.path.join("libros_gutenberg", archivo)

    # Verificar que el archivo exista
    if not os.path.exists(ruta):
        print(f"No se encontró el archivo: {ruta}")
        return

    # Leer archivo
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        texto = f.read().lower()

    # Limpiar signos de puntuación
    for c in '.,;:!?"-()[]{}':
        texto = texto.replace(c, " ")

    # Separar en palabras
    palabras = texto.split()

    # Stopwords simples
    stopwords = {
        'the','a','an','and','or','but','in','on','at','to','for','of','with','by','from',
        'as','is','was','are','were','be','been','being','have','has','had','do','does',
        'did','will','would','could','should','may','might','must','can','this','that',
        'these','those','i','you','he','she','it','we','they'
    }

    # Filtro
    palabras = [p for p in palabras if p not in stopwords and len(p) > 3]

    # Contar frecuencias
    frecuencias = {}
    for palabra in palabras:
        frecuencias[palabra] = frecuencias.get(palabra, 0) + 1

    # Top 20 palabras más comunes
    top20 = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:20]

    print(f"\nResumen de {archivo}:")
    print(", ".join(palabra for palabra, _ in top20))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python resume.py <archivo.txt>")
    else:
        resumir(sys.argv[1])
