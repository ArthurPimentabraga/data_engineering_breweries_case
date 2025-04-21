# Data engineering breweries case

Project to extract brewery data from a API and load it into a mock S3 environment.

## Summary

- [Data engineering breweries case](#data-engineering-breweries-case)
  - [Summary](#summary)
  - [About the project](#about-the-project)
    - [Source data](#source-data)
    - [Data Lake Architecture](#data-lake-architecture)
  - [Monitoring / Alerting](#monitoring--alerting)
  - [How to run](#how-to-run)
    - [Virtual environments creation](#virtual-environments-creation)
    - [Docker](#docker)
      - [How to install docker](#how-to-install-docker)
      - [How to install docker compose](#how-to-install-docker-compose)
      - [How to execute](#how-to-execute)



## About the project

### Source data

| Endpoint                                        | Volumetry | Description                             | 
| ----------------------------------------------- | --------- | --------------------------------------- |
| https://api.openbrewerydb.org/v1/breweries      | ~ 8369    | List of breweries and their information |
| https://api.openbrewerydb.org/v1/breweries/meta | N/A       | API metadata, such as total breweries   |

- Schema example:

```JSON
|-- id: string (nullable = true)
|-- name: string (nullable = true)
|-- brewery_type: string (nullable = true)
|-- street: string (nullable = true)
|-- city: string (nullable = true)
|-- state: string (nullable = true)
|-- postal_code: string (nullable = true)
|-- country: string (nullable = true)
|-- longitude: double (nullable = true)
|-- latitude: double (nullable = true)
|-- phone: string (nullable = true)
|-- website_url: string (nullable = true)
|-- address_1: string (nullable = true)
|-- address_2: string (nullable = true)
|-- address_3: string (nullable = true)
|-- state_province: string (nullable = true)
|-- country_partition: string (nullable = true)
```

### Data Lake Architecture

| Layer  | Format | Partition by | Load type | Transformations | Observations |
| ------ | ------ | --- | --- | --- | --- |
| Bronze | json   | --- | --- | --- | --- |
| Silver | delta  | --- | --- | --- | --- |
| Gold   | delta  | --- | --- | --- | --- |

layer
Format
Partition by
Carregamento
Transformações
Observações

<!-- 
- Explicar a decisão do particionamento.
  - Olhando os metadados, particionar por cidade, estado... as partições iam ficar muito pequenas. Preferi, particionar por pais, e ordenar com delta para otimizar a escrita e leitura, mesmo que a leitura seja filtrando por cidade.
  - A volumetria permite um fulload diário
- Falar sobre a ideia de parametrizar por location para um possível reprocessamento? 
-->

## Monitoring / Alerting

## How to run

<!-- CRIAR UM ARQUIVO SHELL PARA EXECUTAR TUDO DE UMA VEZ? -->

### Virtual environments creation

> Pré-requisitos: Ter instalado o Python3, o pip, o venv e o java

Executar os seguintes comandos:

```Shell
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

JAVA

sudo apt update
sudo apt install openjdk-11-jdk

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

SPARK

wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz

tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark

export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$PATH

<!-- Configurar jars necessários para executar os testes unitários -->
sudo wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -P $SPARK_HOME/jars/


### Docker

#### How to install docker

Para instalar o Docker no Linux, siga estas etapas:

1. **Atualize os pacotes existentes**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instale os pacotes necessários**:
   ```bash
   sudo apt install -y ca-certificates curl gnupg lsb-release
   ```

3. **Adicione a chave GPG oficial do Docker**:
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

4. **Configure o repositório do Docker**:
   ```bash
   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Instale o Docker**:
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

6. **Verifique a instalação**:
   ```bash
   docker --version
   ```

#### How to install docker compose

Para instalar o Docker Compose no Linux, siga estas etapas:

1. Baixe o binário do Docker Compose;
2. Dê permissão de execução ao binário;
3. Verifique a instalação.

```Shell
> sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
> sudo chmod +x /usr/local/bin/docker-compose
> docker-compose --version
```

Isso instalará a versão mais recente do Docker Compose.


#### How to execute 

https://airflow.apache.org/docs/apache-airflow/2.0.2/start/docker.html

Para executar em segundo plano:

```bash
docker-compose up -d
docker-compose ps
```
