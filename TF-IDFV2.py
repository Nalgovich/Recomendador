from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.feature import Tokenizer, StopWordsRemover
import os
import sys

# --------------------------
# 1. INICIAR SPARK
# --------------------------
try:
    spark = SparkSession.builder \
        .appName("TFIDF") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
except Exception as e:
    print("Error iniciando Spark:", e)
    sys.exit(1)

# --------------------------
# 2. LEER ARCHIVOS
# --------------------------
DATA_DIR = "libros_gutenberg"

if not os.path.isdir(DATA_DIR):
    print(f"Error: carpeta {DATA_DIR} no existe.")
    spark.stop()
    sys.exit(1)

datos = []
for archivo in os.listdir(DATA_DIR):
    if archivo.endswith(".txt"):
        path = os.path.join(DATA_DIR, archivo)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read().strip()
                if contenido:
                    datos.append((archivo, contenido))
        except:
            print(f"No se pudo leer {archivo}")

if not datos:
    print("No hay archivos válidos.")
    spark.stop()
    sys.exit(1)

df = spark.createDataFrame(datos, ["doc", "texto"]).cache()

# --------------------------
# 3. LIMPIEZA + TOKENIZACIÓN
# --------------------------
df = df.withColumn(
    "clean",
    F.lower(F.regexp_replace("texto", "[^a-zA-Z0-9\\s]", " "))
)

tokenizer = Tokenizer(inputCol="clean", outputCol="words")
df_words = tokenizer.transform(df)

remover = StopWordsRemover(inputCol="words", outputCol="filtered")
df_words = remover.transform(df_words).select("doc", "filtered").cache()

# --------------------------
# 4. EXPLOTAR PALABRAS
# --------------------------
df_exp = df_words.withColumn("word", F.explode("filtered"))

# --------------------------
# 5. TF MANUAL
# --------------------------
df_TF = df_exp.groupBy("doc", "word").agg(
    F.count("word").alias("tf")
)

# --------------------------
# 6. IDF MANUAL
# --------------------------
df_DF = df_TF.groupBy("word").agg(
    F.count("doc").alias("df")
)

total_docs = df.count()

df_IDF = df_DF.withColumn(
    "idf",
    F.log((F.lit(total_docs) + 1) / (F.col("df") + 1)) + 1 
)

# --------------------------
# 7. TF-IDF FINAL
# --------------------------
df_TFIDF = df_TF.join(df_IDF, "word")
df_TFIDF = df_TFIDF.withColumn(
    "tfidf",
    F.col("tf") * F.col("idf")
)

# --------------------------
# 8. GUARDAR RESULTADOS
# --------------------------
df_TFIDF.write.mode("overwrite").parquet("tfidf")

print("TF-IDF calculado y guardado en tfidf/")

spark.stop()
