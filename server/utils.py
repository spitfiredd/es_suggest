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
