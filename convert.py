import pyspark
from pyspark.sql import SparkSession


db_jar = "C:\\others\\spark\\spark-3.2.1-bin-hadoop3.2\\jars\\postgresql-42.3.4.jar"
driver = "org.postgresql.Driver"
db_url = "jdbc:postgresql://localhost:5432/"
db_name = "recommendationV2"
db_table = "article"
db_user = "postgres"
db_password = "amina"
df_path = "data/random_data.json"

spark = (
    SparkSession.builder.appName("postgres")
    .config("spark.driver.extraClassPath", db_jar)
    .getOrCreate()
)

# read data in json format
df = spark.read.format("json").json(df_path)

df.select(
    "id",
    "title",
    "link",
    "authors",
    "references",
    "year",
).write.format("jdbc").options(
    url=db_url + db_name,
    driver=driver,
    dbtable=db_table,
    user=db_user,
    password=db_password,
).save()
