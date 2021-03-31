from elasticsearch import helpers, Elasticsearch
import csv
from elasticsearch_dsl import connections
from elasticsearch_dsl.query import MultiMatch

from server.models import SamVendors

if __name__ == "__main__":

    es = connections.get_connection()
    SamVendors.init()

    with open('sam_gov_data.csv') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='vendors')
