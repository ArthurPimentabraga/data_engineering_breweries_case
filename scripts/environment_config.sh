# #!/bin/bash

if [ "$(basename "$PWD")" != "data_engineering_breweries_case" ]; then
    echo "You are not in the 'data_engineering_breweries_case' directory. Redirecting..."
    cd ../ || exit 1
fi

# JAVA INSTALLATION
echo "Installing Java..."
sudo apt update
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# SPARK AND DELTA INSTALLATION
echo "Installing Spark and Delta..."
wget https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz

tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /opt/spark

export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$PATH

sudo wget https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars/
sudo wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -P $SPARK_HOME/jars/

# PYTHON INSTALLATION
echo "Installing Python..."
sudo apt update
sudo apt install python3
sudo apt install -y python3-pip

# VIRTUAL ENVIRONMENT CREATION
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# DOCKER INSTALLATION
echo "Installing Docker..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# DOCKER-COMPOSE INSTALLATION
echo "Installing Docker compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version