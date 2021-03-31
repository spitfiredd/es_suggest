import os

import psycopg2
import psycopg2.extras
from elasticsearch_dsl import connections
from dotenv import load_dotenv, find_dotenv

from server.models import SamVendors



load_dotenv(find_dotenv())

PGCONF = os.environ.get('DATABASE_URL')

SQL_QUERY = """
    select 
        id
        , duns
        , duns_plus_four
        , cage_code 
        , legal_business_name 
    from sam.meta
"""


if __name__ == "__main__":

    """Example ETL script to populate the elasticsearch in on local host.
       Data is stored on a database.
    """

    connections.create_connection()

    # # initialize index
    print('Initializing SamVendors...')
    SamVendors.init()

    print('Querying Data from database...')
    with psycopg2.connect(PGCONF) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_QUERY)
            print('Loading ES instance')
            for ele in cur:
                SamVendors(_id=ele['id'],
                           duns=ele['duns'],
                           duns_plus_four=ele['duns_plus_four'],
                           cage_code=ele['cage_code'],
                           name=ele['legal_business_name']
                ).save()
