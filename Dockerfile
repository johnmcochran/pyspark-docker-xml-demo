# Use the Spark Python base image
FROM apache/spark-py:latest
USER root

# Download the spark-xml JAR
RUN wget https://repo1.maven.org/maven2/com/databricks/spark-xml_2.12/0.15.0/spark-xml_2.12-0.15.0.jar \
    -P /opt/spark/jars/

# Set environment variables for Spark
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Create a writable directory for pip
ENV PYTHONUSERBASE=/app/.local

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script into the container
COPY app.py app.py

# Copy requirements file into container
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install --user --no-cache-dir -r requirements.txt

RUN mkdir -p /output

# Default command to run the script
CMD ["spark-submit", "app.py"]
