# data_engineering_breweries_case

<!-- Sumário? -->

## How to run

<!-- CRIAR UM ARQUIVO SHELL PARA EXECUTAR TUDO DE UMA VEZ? -->

### Virtual environments creation

> Pré-requisitos: Ter instalado o Python3, o pip e o venv

Executar os seguintes comandos:

```Shell
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

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
