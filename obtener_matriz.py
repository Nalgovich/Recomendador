# obtener_matriz.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os
import sys

spark = (
    SparkSession.builder
    .appName("Similitud")
    .master("local[*]")
    .getOrCreate()
)

# -------------------------------
# 1. Buscar carpeta TF-IDF válida
# -------------------------------
posibles = ["tfidf", "tfidf_data", "tfidf_ml_data", "tfidf_hibrido"]

ruta_tfidf = None
for carpeta in posibles:
    if os.path.exists(carpeta):
        ruta_tfidf = carpeta
        break

if ruta_tfidf is None:
    print("\n ERROR: No se encontró ninguna carpeta TF-IDF.")
    print("   Carpetas válidas esperadas:", posibles)
    print("   Ejecuta: ls -d */  para ver las carpetas.\n")
    spark.stop()
    sys.exit(1)

print(f"Usando carpeta TF-IDF encontrada: {ruta_tfidf}\n")

# -------------------------------
# 2. Cargar TF-IDF (formato de TF-IDFV2.py)
# -------------------------------
df = spark.read.parquet(ruta_tfidf)

# -------------------------------
# 3. Calcular norma por documento
# -------------------------------
normas = (
    df.groupBy("doc")
      .agg(F.sqrt(F.sum(F.col("tfidf")**2)).alias("norma"))
)

# -------------------------------
# 4. Producto punto entre documentos
# -------------------------------
producto = (
    df.alias("a")
      .join(df.alias("b"), F.col("a.word") == F.col("b.word"))
      .select(
          F.col("a.doc").alias("doc1"),
          F.col("b.doc").alias("doc2"),
          (F.col("a.tfidf") * F.col("b.tfidf")).alias("dot")
      )
)

numerador = (
    producto.groupBy("doc1", "doc2")
            .agg(F.sum("dot").alias("dot_product"))
)

# -------------------------------
# 5. Unir normas y calcular similitud
# -------------------------------
resultado = (
    numerador
    .join(normas.withColumnRenamed("doc", "doc1")
                .withColumnRenamed("norma", "norma1"), "doc1")
    .join(normas.withColumnRenamed("doc", "doc2")
                .withColumnRenamed("norma", "norma2"), "doc2")
)

resultado = resultado.withColumn(
    "similitud",
    F.col("dot_product") / (F.col("norma1") * F.col("norma2"))
).select("doc1", "doc2", "similitud")

# -------------------------------
# 6. Guardar resultados
# -------------------------------
resultado.write.mode("overwrite").parquet("similitudes")

print("Similitudes calculadas y guardadas en 'similitudes/'\n")
spark.stop()
