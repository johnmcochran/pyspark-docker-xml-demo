import requests
from pyspark.sql import SparkSession

def spark_init():
    # Initialize SparkSession
    spark = SparkSession.builder.appName("PublicAPIExample").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

spark = spark_init()

# Hit a public API
response = requests.get("https://alerts.weather.gov/cap/in.php?x=1")
print('----RESPONSE---------------------------------------------------')
print('===============================================================')
print('===============================================================')
print('===============================================================')

print(response.text)
data = response.text

# Check if the request was successful
if response.status_code == 200:
    # Save the XML content to a file
    with open("weather_data.xml", "w", encoding="utf-8") as file:
        file.write(data)
    print("File saved as 'weather_data.xml'")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")

# Parse the data (example: convert to RDD)
#rdd = spark.sparkContext.parallelize(data)
df = spark.read.format('xml').option('rowTag', 'a').load('weather_data.xml')


print('----SCHEMA---------------------------------------------------')
print('===============================================================')
print('===============================================================')
print('===============================================================')
print(df.schema)
# Save a simple TXT file
df.write.mode("overwrite").json("/output/todos.json")

output_df = spark.read.format('json').load("/output/todos.json").cache()
print('----DF HEAD---------------------------------------------------')
print('===============================================================')
print('===============================================================')
print('===============================================================')
print(output_df.filter("_corrupt_record IS NOT NULL").show(truncate=False))

print("Job completed! Output saved to /output/todos.json")
spark.stop()
