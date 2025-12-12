from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys

spark = (
    SparkSession.builder
    .appName("Recomendar")
    .master("local[*]")
    .getOrCreate()
)

# ----------------------------------------------------------
# Si no pasas un argumento: lista los libros disponibles
# ----------------------------------------------------------
if len(sys.argv) < 2:
    df = spark.read.parquet("tfidf")
    
    print("\nLibros disponibles:\n")
    for row in df.select("doc").distinct().collect():
        print(" -", row["doc"])
    
else:
    # ------------------------------------------------------
    # si pasas un argumento: recomendar libros parecidos
    # ------------------------------------------------------
    libro = sys.argv[1]
    df = spark.read.parquet("similitudes")

    print(f"\nRecomendaciones para: {libro}\n")

    recomendaciones = (
        df.filter(col("doc1") == libro)
          .filter(col("doc1") != col("doc2")) 
          .orderBy(col("similitud").desc())
          .limit(10)
          .collect()
    )

    for i, row in enumerate(recomendaciones, start=1):
        print(f"{i}. {row['doc2']}")

spark.stop()
