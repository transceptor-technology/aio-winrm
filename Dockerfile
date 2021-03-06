FROM ubuntu:rolling

RUN apt update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt install -y --no-install-recommends kinit krb5-user python3 build-essential python3-dev python3-pip libkrb5-dev
COPY requirements.txt .
RUN pip3 install setuptools wheel # pykerberos: ModuleNotFoundError: No module named 'setuptools'
RUN pip3 install -r requirements.txt
