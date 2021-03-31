
import json

from elasticsearch_dsl import connections
from flask import Blueprint, Response, render_template, request, current_app

from server.models import SamVendors


search_bp = Blueprint('search', __name__)


@search_bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    """ GET endpoints that runs full text search.

    Returns:
        flask.Response: Search results, serialized as JSON.
    """

    connections.create_connection()

    name = request.args.get('name')
    size = request.args.get('size', 15)
    sam_vendors = SamVendors()
    output = sam_vendors.auto_complete(name, 'legal_business_name', size=size)
    return Response(json.dumps(output), mimetype='application/json')


@search_bp.route('/')
def search():
    """Serve web page for to run search as you type in browser

    Returns:
        flask.render_template: renders search template.
    """
    title = "Search as you type powered by Elasticsearch."
    return render_template('search.html', title=title)
