
import json

from elasticsearch_dsl import connections
from flask import Blueprint, Response, render_template, request, redirect, url_for

from server.elastic_models import SamVendorsIndex
from server.database_models import SamVendors
from server.forms import UpdateByCageForm
from server.extensions import db


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
    sam_vendors = SamVendorsIndex()
    results = sam_vendors.auto_complete(name, 'legal_business_name', size=size)
    return Response(
        json.dumps(results),
        status=200,
        mimetype='application/json'
    )


@search_bp.route('/')
def search():
    """Serve web page for to run search as you type in browser

    Returns:
        flask.render_template: renders search template.
    """
    title = "Search as you type powered by Elasticsearch."
    return render_template('search.html', title=title)


@search_bp.route('/update', methods=('GET', 'POST'))
def update():
    form = UpdateByCageForm()
    if form.validate_on_submit():
        vendor = SamVendors.query.filter_by(cage_code=form.cage.data).first()
        vendor.legal_business_name = form.name.data

        db.session.add(vendor)
        db.session.commit()
        return redirect(url_for('search.search'))
    return render_template('update.html', form=form)
