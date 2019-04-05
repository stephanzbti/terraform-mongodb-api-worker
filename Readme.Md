# TerraForm - MongoDB - APIRest (SendMessage) - Worker (ReaderMessage)

## Aplicação

Está aplicação tem o objetivo de ler uma requisição HTTP Post e envia-lá para o AWS SQS, e em seguida o Worker irá reconhecer essa mensagem e irá processa-lá armazenando no banco de dados MongoDB e deletando-a da fila.

Para que seja executado tudo corretamente é necessário configurar o ambiente primeiro, para que, em seguida, rode a aplicação por inteiro. Para isso é necessário que seja feita a configuração na seguinte ordem:

1. Terraform
1. MongoDB
1. APIRest
1. Worker

Todas as configurações necessárias de cada serviço está descrito a baixo. Sendo totalmente necessária a execução de todas elas para que a aplicação execute perfeitamente.

## TerraForm

### Documentação TerraForm  

O TerraForm existente neste projeto está configurado para criar o serviço completo do SQS necessário para que seja feita a execução completa desta aplicação e junto salvar o TSFile em um Bucket S3. É necessário configurar as credenciais de acesso de cada arquivo, para isso será necessário modificar os arquivos **main.tf** e **terraform.tf**, nas seguintes linhas descritar abaixo:

```
    # terraform.tf -> Responsável por salvar o TSFile no S3

    bucket = "BUCKETNAME" -> Nome do Bucket S3
    key = "PATH/TS/FILE" -> Destino do arquivo TSFile
    access_key = "ACCESS_KEY" -> Chave de acesso da AWS
    secret_key = "SECRET_KEY" -> Secret de acesso da AWS
    region = "REGION_AWS" -> Região do Bucket da AWS

    # main.tf

    access_key = "ACCESS_KEY" -> Chave de acesso da AWS
    secret_key = "SECRET_KEY" -> Secret de acesso da AWS
    region = "REGION_AWS" -> Região do Bucket da AWS
    
```

### Depêndencias TerraForm

Será necessário criar o bucket S3 que será salvo o TSFile, desta forma os arquivos gerados pelo TerraForm serão armazenados com segurança e fácil acesso á todos permitidos.

### Execução TerraForm

Para executar o TerraForm é necessário digitar os seguintes comandos:

```
$ cd Terraform
$ sudo docker-compose build terraform
$ sudo docker-compose run terraform
[DOCKER] # terraform apply
```

### IAM Policy SQS

É necessário criar uma política no IAM para que seja liberado o acesso ao TerraForm para criar á infraestrutura do SQS. A permissão de política minima necessária para se criar o SQS com terraforma está descrita abaixo:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:TagQueue",
                "sqs:GetQueueUrl",
                "sqs:GetQueueAttributes",
                "sqs:ListQueueTags",
                "sqs:CreateQueue",
                "sqs:SetQueueAttributes"
            ],
            "Resource": "*"
        }
    ]
}
```

Caso não tenha conhecimento em JSON, você pode configurar essa política utilizando o painel de console do IAM. É necessária configurar uma política que tenha acesso ao serviço do SQS, apenas, e que tenha permissão de **TagQueue**, **GetQueueUrl**, **GetQueueAttributes**, **ListQueueTags**, **CreateQueue** e **SetQueueAttributes**, desta forma o terraforms irá comunicar com sucesso a AWS.

É necessário criar uma política no IAM para que seja liberado o acesso ao TerraForm para salvar o arquivo TFState, sendo necessário modificar a política para o bucket correto. A permissão de política minima necessária para se salvar o arquivo com terraforma está descrita abaixo: 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::mybucket" -> BUCKET_DE_DESTINO
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::mybucket/path/to/my/key" -> BUCKET_DE_DESTINO_TSFILE/DESTINO_TS_FILE
    }
  ]
}
```

Caso não tenha conhecimento em JSON, você pode configurar essa política utilizando o painel de console do IAM. É necessária configurar uma política que tenha acesso ao serviço do S3, apenas, e que tenha permissão de **ListBucket**, **GetObject** e **PutObject** desta forma o terraforms irá comunicar com sucesso a AWS.


## MongoDB

### Documentação MongoDB

Este MongoDB está configurado para ser executado sem senha, sendo necessário fazer as modificações necessárias para que seja feita a execução correta de usuários, ReplicaSet e certificados SSH. Ele está configurado para ser executado o minimo possível para que exista conexão junto a aplicação, serviço e Clientes MongoDB como NoSQLBooster.

### Execução MongoDB

```
$ cd MongoDB
$ sudo docker build -t mongodb:latest .
$ sudo docker run -dti -p 27017:27017 mongodb:latest
```

## APIRest

Está APIRest é uma aplicação responsável pela geração de uma fila de mensagems no serviço SQS da AWS. Está fila de mensagem é padrão, sendo utilizada para armezenar informações que outras aplicações poderiam usar, caso fosse necessária, ou então para fazermos processamento em grande escala de uma forma organizada e sem a necessidade de se preocupar com a ordem em que se chega a mensagem, sendo a organização da fila e do acesso a cada elemento, controlada pela AWS, que tem como tipo de serviço o compartilhamento de responsabilidades, neste caso o de gerir a aplicação de fila e de acesso á fila.

### Documentação API

Está API Rest conta com apenas 1 EndPoint para ser utilizado. Á descrição da sua utilização está abaixo e em seu código também existe o detalhamento do EndPoint e como utiliza-lo.

**EndPoint**: '**/api/v1/sender/sqs**'
**Payload**:

```
{
	"title": STRING, -> Titulo da Mensagem
	"author": STRING, -> Author do Mensagem
	"ttl": INT, -> Time to Leave, em semanas
	"message": STRING -> Mensagem
}
```

Para configurar as variáveis de ambientes desta aplicação é necessário modificar, dependendo da forma que irá executar a aplicação, Docker-Compose ou Dockerfile as variáveis de ambiente, sendo elas descritas abaixo.

```
SQSURL -> SQS URL informada no Painel do SQS da AWS. DEFAULT=''
BOTO3_AWS_KEY_ID -> AWS Key ID do usuário com as politícas de permissões necessárias para acessar a aplicação, segue abaixo á política minima de acesso. DEFAULT=''
BOTO3_AWS_SECRET_KEY -> AWS Secret Key do usuário infomado acima. DEFAULT=''
BOTO3_AWS_REGION_NAME -> AWS Region Name da localização em que se encontra o serviço SQS. DEFAUL=''
LOGGER_LEVEL -> Definição do Logger Level do módulo Loggin do Python. DEFAULT=10 [Loggin](https://docs.python.org/3/library/logging.html)
PORT -> Porta que irá rodar a API Rest. DEFAULT=3000
```

### Estrutura dos dados

Esta aplicação foi estruturada pensando de maneira simples e fácil de dar manutenção, portanto sendo da seguinte maneira:

```
start.py
src/
    - controller/
        - sqs/
            - routes/
                - sender.py

```

### Depêndencia de módulos

Para se utilizar está API Rest será necessário a intalação dos sequintes módulos, descritas também no requirements.txt:

```
aniso8601
boto3
botocore
click
docutils
itsdangerous
jmespath
python-dateutil
python-decouple
python-dotenv
pytz
s3transfer
six
urllib3
Flask-RESTful
Flask
Jinja2
MarkupSafe
Werkzeug
```

### Execução da Aplicação

Para se executar está aplicação, apenas, é necessário fazer todas as configurações propostas acima e após isto, executar com os seguintes comandos:

```
$ cd APIRest
$ sudo docker build -t IMAGE_NAME:TAG .
$ sudo docker run -dti -p 3000:3000 IMAGE_NAME
```

É necessário substituir o IMAGE_NAME pelo nome da imagem que deseja executar, desta forma organizando suas imagens e sempre deixando a mais atual com a tag latest, é necessário modificar também a porta que irá executar, caso você tenha mudado.

## Worker

Este Worker é responsável por consumir a informação na fila, e em seguida salva-la no banco e deleta-la, para que não seja processada novamente. Desta forma é possível criar uma aplicação que faça leitura de certos dados, como transações e possa fazer em sequência sem que uma atrapalhe a outra, portanto sendo escalável.

### Documentação Worker

Este Worker é um serviço pelo qual fica analisando se existe uma mensagem na fila, e se caso exista, lê a mensagem, insere no banco e remove a mensagem da fila.

Para configurar as variáveis de ambiente deste serviço é necessário modificar, dependendo da forma que irá executar a aplicação, Docker-Compose ou Dockerfile as variáveis de ambiente, sendo elas descritar abaixo.

```
SQSURL -> SQS URL informada no Painel do SQS da AWS. DEFAULT=''
BOTO3_AWS_KEY_ID -> AWS Key ID do usuário com as politícas de permissões necessárias para acessar a aplicação, segue abaixo á política minima de acesso. DEFAULT=''
BOTO3_AWS_SECRET_KEY -> AWS Secret Key do usuário infomado acima. DEFAULT=''
BOTO3_AWS_REGION_NAME -> AWS Region Name da localização em que se encontra o serviço SQS. DEFAUL=''
LOGGER_LEVEL -> Definição do Logger Level do módulo Loggin do Python. DEFAULT=10
MONGODB -> Denife qual banco será acessado para armazenar as mensagens da fila. DEFAULT='mongodb://localhost:27017/MaxMilhas'
```

### Estrutura dos dados

Esta aplicação foi estruturada pensando de maneira simples e fácil de dar manutenção, portanto sendo da seguinte maneira:

```
start.py -> Ponto de partida da aplicação
src/
    - index.py -> Orquestrador da aplicação
    - configs/
        - loadBD.py -> Criação do banco de dados
    - controller/
        - consumer/
            - consumer.py -> Consumidor do SQS
    - dao/
        - sugestion.py -> Schema Sugestion
```

### Depêndencia de módulos

Para se utilizar está API Rest será necessário a intalação dos sequintes módulos, descritas também no requirements.txt:

```
python-decouple
boto3
pymongo
```

### IAM Policy SQS

É necessário criar a política miníma de acesso ao SQS para que o acesso aos recursos do SQS da AWS sejam feitas com sucesso. Abaixo descrevo a política miníma necessária, em JSON:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage",
                "sqs:SendMessage"
            ],
            "Resource": "*"
        }
    ]
}
```

Caso não tenha conhecimento em JSON, você pode configurar essa política utilizando o painel de console do IAM. É necessária configurar uma política que tenha acesso ao serviço do SQS, apenas, e que tenha permissão de **DeleteMessage**, **ReceiveMessage** e **SendMessage**, desta forma sua aplicação irá comunicar com sucesso a AWS.

### Execução da Aplicação

Para se executar este serviço, apenas, é necessário fazer todas as configurações propostas acima e após isto, executar com os seguintes comandos:

```
$ cd Worker
$ sudo docker build -t IMAGE_NAME:TAG .
$ sudo docker run -dti IMAGE_NAME
```

É necessário substituir o IMAGE_NAME pelo nome da imagem que deseja executar, desta forma organizando suas imagens e sempre deixando a mais atual com a tag latest.

## Execução da aplicação completa

Esta aplicação foi desenvolvida para ser executada em cima de um contâiner mais especificamente um Docker, porém para que ele funcione perfeitamente é necessário que seja executado via docker-compose apenas uma vez, sendo o ambiente totalmente configurado apartir do docker-compose. Para que a aplicação execute corretamente é necessário que seja feita a configuração das variáveis de ambiente corretamente como descrita acima em cada serviço que irá executar, após essa configuração é necessário executar os passos abaixo para que a aplicação execute.

### Instalação do Docker Linux e do Docker-Compose Linux

O tutorial de instalação do Docker está totalmente descrito no site da própria Docker que administra a aplicação do Docker e do Docker-Compose.

[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
[Docker-Compose](https://docs.docker.com/compose/install/)

### Inicialização da Aplicação

Para que a aplicação seja iniciada é necessário estar na pasta raiz da aplicação e executar os seguintes comandos:

```
$ sudo docker-compose build
$ sudo docker-compose up -d
```

Após a execução de ambos os comandos seu contâiner irá executar e estara executando perfeitamente.