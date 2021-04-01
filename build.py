import os
import csv

import psycopg2
from psycopg2.extras import execute_values
from elasticsearch_dsl import connections
from dotenv import load_dotenv, find_dotenv

from server.extensions import db
from server.app import create_app
from server.elastic_models import SamVendorsIndex
from server.database_models import SamVendors


load_dotenv(find_dotenv())


if __name__ == "__main__":

    app = create_app()

    # create tables on the database
    with app.app_context(): 
        db.drop_all()
        db.create_all()


    # load data
    with open("sam_gov_data.csv") as f:
        data = [tuple(line) for line in csv.reader(f)]


    insert_statment = """
        INSERT INTO sam_vendors(
            duns,
            duns_plus_four,
            cage_code,
            legal_business_name,
            elec_govt_bus_poc_email,
            mailing_address_line1,
            mailing_address_line2,
            mailing_address_city,
            mailing_address_state,
            mailing_address_zip,
            mailing_address_zip_plus_four,
            mailing_address_country) 
        VALUES %s
        """
    # insert data into database
    with psycopg2.connect(os.environ.get('DATABASE_URL')) as conn:
        with conn.cursor() as cursor:
            execute_values(cursor, insert_statment, data[1::])
            conn.commit()

    # create elasticsearch index
    es = connections.create_connection(hosts=['localhost'], timeout=20)
    SamVendorsIndex._index.delete()
    SamVendorsIndex.init()
