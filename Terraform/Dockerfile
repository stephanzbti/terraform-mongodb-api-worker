FROM ubuntu:latest

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN apt-get update
RUN apt-get install -y unzip
RUN apt-get install -y wget
RUN wget https://releases.hashicorp.com/terraform/0.11.13/terraform_0.11.13_linux_amd64.zip
RUN unzip terraform_0.11.13_linux_amd64.zip
RUN mv terraform /usr/local/bin/

RUN ["terraform", "init"]