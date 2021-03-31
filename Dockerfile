FROM python:3.8-buster

# build dependencies for postgres client
RUN apt-get -qq -y update && \
    apt-get -qq -y install \
        build-essential \
        libpq-dev \
        postgresql-client \
        postgresql-common

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /server

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD CMD ["flask", "run"]