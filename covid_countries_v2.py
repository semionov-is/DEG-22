from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, lag, round, max
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Python Spark SQL COVID analysis").getOrCreate()
df = spark.read.csv("owid-covid-data.csv", header=True, inferSchema=True)


march_31_data = df.filter((col('date') == '2021-03-31'))
march_31_data = march_31_data.withColumn("percentage_infected", (col("total_cases") / col("population")) * 100)
march_31_data = march_31_data.withColumn("percentage_infected", round(col("percentage_infected"), 2))
result = march_31_data.select("iso_code", "location", "percentage_infected")

result = result.orderBy("percentage_infected", ascending=False).limit(15)
result = result.withColumnRenamed("location", "страна")
result = result.withColumnRenamed("percentage_infected", "процент переболевших")

print("15 стран с наибольшим процентом переболевших на 31.03.2021:")
result.show()


df_march = df.filter((df.date >= "2021-03-25") & (df.date <= "2021-03-31"))
df_march = df_march.filter(~df_march.location.isin(["World", "Europe", "European Union", "Asia","North America",
                                                    "South America", "Africa"]))

top_10_countries = df_march.groupBy("location") \
                    .agg(max("new_cases").alias("max_new_cases"), 
                         max("date").alias("date")) \
                    .orderBy(desc("max_new_cases")) \
                    .limit(10)

top_10_countries = top_10_countries.withColumnRenamed("date", "число")
top_10_countries = top_10_countries.withColumnRenamed("location", "страна")
top_10_countries = top_10_countries.withColumnRenamed("max_new_cases", "количество новых случаев")

print("Top 10 стран с максимальным зафиксированным кол-вом новых случаев за последнюю неделю марта (25-31.03) 2021:")
top_10_countries.show()


df_russia = df.filter((df.location == "Russia") & (df.date >= "2021-03-24") & (df.date <= "2021-03-31"))
df_russia = df_russia.orderBy(df_russia.date)

window = Window.orderBy(df_russia.date)

df_russia = df_russia.withColumn("number_of_new_cases_yesterday", lag(col("new_cases"), 1).over(window))
df_russia = df_russia.withColumn("delta", col("new_cases") - col("number_of_new_cases_yesterday"))
df_russia = df_russia.select("date", "number_of_new_cases_yesterday", "new_cases", "delta")

df_russia = df_russia.filter(df_russia.date >= "2021-03-25")

df_russia = df_russia.withColumnRenamed("date", "число")
df_russia = df_russia.withColumnRenamed("number_of_new_cases_yesterday", "кол-во новых случаев вчера")
df_russia = df_russia.withColumnRenamed("new_cases", "кол-во новых случаев сегодня")
df_russia = df_russia.withColumnRenamed("delta", "дельта")

print("Изменение случаев относительно предыдущего дня в России за последнюю неделю марта (25-31.03) 2021:")
df_russia.show()


spark.stop()
