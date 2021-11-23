FROM ubuntu:20.04

# Set up
RUN apt update -y  &&  apt upgrade -y && apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt install -y curl python3.9 git python3-pip unixodbc unixodbc-dev

# Add SQL Server ODBC Driver 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17


# Set up app
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0"]
