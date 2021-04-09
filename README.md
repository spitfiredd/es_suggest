# Getting Start

## Install and setup environment

Run the following commands:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Start services

To run this application we need to install Postgres, Elasticsearch and Redis. Instead of installing
onto our machine we will docker images.

1. Start Services (use docker image)
    * docker-compose up
2. In a separate terminal activate your virtual env and run the `build.py` script from the root directory to load the database and create the index.

## Start pgsync

Run the following command to sync postgres and elasticsearch.

```
bootstrap --config /sync/schema.json
pgsync --config /sync/schema.json --daemon
```

The first command will add a trigger to the table defined in the `schema.json` file. The second script will run a backgroud daemon monitoring changes in your database and making the necessary changes in your Elasticsearch index.  If this is the first time runnning it, it will load all the records.

## Logstash

You can also run logstash in the background to monitor changes in the database.  This is included in the `docker-compose.yml` file under the `logstash` section.

## Data

The data is sourced from [SAM.gov](https://sam.gov/SAM/pages/public/extracts/samPublicAccessData.jsf).

## Start Application

In a third terminal we will start the flask application.

1. Start application with `flask run`
2. Navigate to `localhost:5000` and test out by entering company names into the search box.
