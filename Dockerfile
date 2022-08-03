## syntax=docker/dockerfile:1

## python 3.9x needed due to an error I didn't log
FROM python:3.9

## set shell to bash instead of sh
SHELL ["/bin/bash", "-ec"]

## the tutorials include these; todo- figure out what they do
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## who doesn't love a "stuff" directory!  :)
WORKDIR /sr_project_stuff/code
RUN mkdir /sr_project_stuff/logs
RUN mkdir /sr_project_stuff/DBs

## set up the python environment
COPY ./config/requirements.txt /sr_project_stuff/code/
RUN pip install -r ./requirements.txt  
