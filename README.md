README – Sistema de Procesamiento, Análisis y Recomendación de Libros
con PySpark

Integrantes en la elaboracion del proyecto:
Higuera Avila Cesar,
Ramirez de la O Josue Alberto,
Santos Contreras Brian Alejandro

Este proyecto implementa un pipeline completo para:

-   descargar libros de Project Gutenberg,
-   procesarlos mediante TF-IDF,
-   calcular similitudes entre los libros,
-   generar recomendaciones basadas en contenido,
-   y producir resúmenes simples basados en frecuencia de palabras.

Todo el procesamiento se realiza con PySpark.

Estructura del Proyecto:

/libros_gutenberg /tfidf /similitudes

descargar.py TF-IDFV2.py obtener_matriz.py recomienda.py resume.py

1.  descargar.py Descarga libros del 1 al 100 desde Project Gutenberg y
    los guarda en ‘libros_gutenberg/’.

2.  TF-IDFV2.py Procesa todos los libros y calcula TF-IDF manualmente
    usando PySpark. Guarda los resultados en ‘tfidf/’.

3.  obtener_matriz.py Utiliza los valores TF-IDF para calcular la
    similitud coseno entre los libros. Guarda los resultados en
    ‘similitudes/’.

4.  recomienda.py "Libro27.txt" Recomienda los libros más parecidos a uno dado usando
    la matriz de similitudes.
    #Ejemplo de ejecucion antes del recomienda

6.  resume.py "Libro27.txt" Genera un resumen simple mostrando las palabras más
    frecuentes (sin stopwords) de un libro específico.
    #Ejemplo de ejecucion antes del Genera.

Flujo de Uso: 1. Ejecutar ‘descargar.py’ 2. Ejecutar ‘TF-IDFV2.py’ 3.
Ejecutar ‘obtener_matriz.py’ 4. Ejecutar ‘recomienda.py’ 5. (Opcional)
Ejecutar ‘resume.py’
