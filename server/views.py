
import json

from flask import Blueprint, Response, render_template, request, current_app
from elasticsearch_dsl import connections
from elasticsearch_dsl.query import MultiMatch

from server.models import SamVendors


search_bp = Blueprint('search', __name__)


def build_elastic_results_dict(response):
    """Convert response object to dict for JSON serialization.

    Args:
        response (elasticsearch_dsl.Search): search results

    Returns:
        list of dicts: query results.
    """
    output = []
    for ele in response:
        data = ele.to_dict()
        data['id'] = ele.meta.id
        output.append(data)
    return output


@search_bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    """ GET endpoints that runs full text search.

    Returns:
        flask.Response: Search results, serialized as JSON.
    """

    connections.create_connection()

    name = request.args.get('name')
    size = request.args.get('size', 15)
    s = SamVendors.search()

    s.query = MultiMatch(
        query=name,
        type="bool_prefix",
        fields=["legal_business_name", "legal_business_name._2gram", "legal_business_name._3gram"],
    )
    s = s.extra(size=size)
    # log the search JSON that is sent to Elasticsearch.
    # see https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
    # for more info on constructing queries.
    current_app.logger.info(f"search json: {s.to_dict()}")
    response = s.execute()
    output = build_elastic_results_dict(response)
    return Response(json.dumps(output), mimetype='application/json')


@search_bp.route('/')
def search():
    """Serve web page for to run search as you type in browser

    Returns:
        flask.render_template: renders search template.
    """
    title = "Search as you type powered by Elasticsearch."
    return render_template('search.html', title=title)
