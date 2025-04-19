# Use a mesma imagem base definida no docker-compose
FROM apache/airflow:2.0.2

USER root

# Configuração do Java e Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=hadoop3
ENV SPARK_HOME=/opt/spark
ENV PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH

# Instale o Java, Apache Spark e o pacote procps
RUN apt-get update && apt-get install -y wget openjdk-11-jdk ca-certificates-java procps && \
    apt-get install -f -y && \
    dpkg --configure -a && \
    update-ca-certificates -f && \
    wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-${HADOOP_VERSION} $SPARK_HOME && \
    ln -s $SPARK_HOME/bin/spark-submit /usr/bin/spark-submit && \
    ln -s $SPARK_HOME/bin/spark-shell /usr/bin/spark-shell && \
    rm spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz

RUN mkdir -p /home/airflow/.ivy2 && chown airflow:airflow /home/airflow/.ivy2

# Baixe as dependências do Hadoop, AWS SDK e Delta Lake
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.524/aws-java-sdk-bundle-1.12.524.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar -P $SPARK_HOME/jars/

# Instale o PySpark no ambiente Python
RUN /usr/local/bin/pip install pyspark