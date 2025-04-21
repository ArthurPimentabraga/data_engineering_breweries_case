# Data engineering breweries case

Project to extract brewery data from a API and load it into a mock S3 environment.

<br>

## Summary

- [Data engineering breweries case](#data-engineering-breweries-case)
  - [Summary](#summary)
  - [About the project](#about-the-project)
    - [Source data](#source-data)
    - [Data Lake Architecture](#data-lake-architecture)
  - [Monitoring / Alerting](#monitoring--alerting)
    - [Data quality](#data-quality)
    - [Pipeline failures](#pipeline-failures)
  - [How to run](#how-to-run)
    - [Environment configuration](#environment-configuration)
      - [Java](#java)
      - [Spark and Delta](#spark-and-delta)
      - [Python and Pip](#python-and-pip)
      - [Virtual environments creation](#virtual-environments-creation)
      - [Docker](#docker)
      - [Docker compose](#docker-compose)
    - [How to execute](#how-to-execute)

<br>

## About the project

### Source data

| Endpoint                                        | Volumetry | Description                             | 
| ----------------------------------------------- | --------- | --------------------------------------- |
| https://api.openbrewerydb.org/v1/breweries      | ~ 8.369   | List of breweries and their information |
| https://api.openbrewerydb.org/v1/breweries/meta | N/A       | API metadata, such as total breweries   |

Schema example:

```TEXT
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
```

<br>

### Data Lake Architecture

| Layer  | Format | Partition by      | Load type | Transformations                                                    | Observations                                                                                                  |
| ------ | ------ | ----------------- | --------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Bronze | json   | country_partition | Full load | Creation of `country_partition` <br> column from `country` column. | For correct partitioning, the country_partition <br> is created in a format without spaces and in lowercase. |
| Silver | delta  | country_partition | Full load | N/A | A physical ordering of the data is done <br> using `Z-ORDER` in the `city` column. |
| Gold   | delta  | country_partition | Full load | Aggregating data to get the <br> number of breweries <br> by `brewery_type` and `country`. | N/A |  

> **Partitioning explanation:** <br>
> One of the project requirements was to partition data by breweries location. Knowing this, and because the data volume was low, the partitioning was done using the `country` field, to prevent the creation of very small partitions (as would be the case if the partitioning were done by city or state). <br>
> To improve performance when reading the data, if a user wanted to filter by another location field, such as city, the data was physically sorted using `Z-ORDER` in the `city` column.

<br>

## Monitoring / Alerting

### Data quality

For a data quality implementation, `Great Expectations` would be used. With this tool, it is possible to write a list of validation cases that you want to do with the data that is being saved in each layer. Example:

- Case 1:
  - Column: name
  - Validation: `expect_column_values_to_not_be_null`
  - Explanation: Will validate if any value of this column is null. If there is, this validation will be considered as **failed**.

- Case 2:
  - Column: id
  - Validation: `expect_column_values_to_be_unique`
  - Explanation: Will validate if each value of this column is unique. If there is a duplicate, this validation will be considered as **failed**.

A job to execute data quality validations can be created and executed at the end of the dag after all the main jobs. If any validation fails, a `webhook` will be configured to notify those responsible for the data.

<br>

### Pipeline failures

To alert about possible pipeline failures, a `webhook` would be configured to notify those responsible for the DAG.

This notification can be sent to the team's main communication channel, such as **e-mail**, **Slack**, **Microsoft Teams**, among others.

<br>

## How to run

### Environment configuration

The project is executed using some solutions, such as: Docker for Airflow and S3; Virtual environment for installing some necessary libraries and running unit tests; Use of Spark for data processing.

To facilitate this process, shell scripts were created to configure the environment and run the project. They are located in the `scripts` directory. But you can also follow the step-by-step instructions below.

- [Shell script to enviroment configuration](scripts/environment_config.sh)
- [Shell script to initialize environmet](scripts/initialize_environment.sh)
- [Shell script to stop environment](scripts/stop_environment.sh)

| Prerequisites  | Version | 
| -------------- | ------- | 
| Java           | 11      | 
| Spark          | 3.4.1   | 
| Delta          | 2.4.0   |
| Python         | 3.x.x   |
| Pip            | N/A     |
| Docker         | N/A     |
| Docker-compose | N/A     |

> Note: The following steps are instructions for installing resources in the Linux environment

#### Java

```Shell
sudo apt update
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

#### Spark and Delta

```SHELL
wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz

tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark

export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$PATH

sudo wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -P $SPARK_HOME/jars/
```

> Note: The delta `.jar` files must be configured in the `$SPARK_HOME/jars/` directory as done in the script above.

#### Python and Pip

```Shell
sudo apt update
sudo apt install python3
sudo apt install -y python3-pip
```

#### Virtual environments creation

```Shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Docker

```Shell
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Docker compose

```Shell
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

<br>

### How to execute 

To initialize and stop the docker containers, simply run the following scripts:

- [Shell script to initialize environment](scripts/initialize_environment.sh)
- [Shell script to stop environment](scripts/stop_environment.sh)

After running the initialization script, the airflow webserver will be available at the address `http://localhost:8080/`.

Access login:
- User: airflow
- Password: airflow