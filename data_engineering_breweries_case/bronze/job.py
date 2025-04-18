import logging
from pyspark.sql import SparkSession

class BronzeJob:
    def __init__(self):
        pass

    def run(self):
        # Configuração do Spark
        spark = SparkSession.builder.appName("ExampleJob").getOrCreate()

        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Exemplo de DataFrame
        data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
        columns = ["Name", "Age"]
        df = spark.createDataFrame(data, columns)

        # Exibe o DataFrame no log
        logger.info("Exibindo o DataFrame:")
        df.show()

# Adicione este bloco para executar o método run
if __name__ == "__main__":
    job = BronzeJob()
    job.run()