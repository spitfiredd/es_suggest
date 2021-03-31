# Getting Start

## Install and setup environment

Run the following commands:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Create index and load data

1. Start elasticsearch (use docker image)
    * docker-compose up
2. Run the `build.py` script from the root directory to create the index and populate the index.

## Start Application

1. Start application with `flask run`
2. Navigate to `localhost:5000` and test out by entering company names into the search box.
