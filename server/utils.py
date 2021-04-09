def build_elastic_results_dict(response, remove_keys=None):
    """Convert response object to dict for JSON serialization.

    Args:
        response (elasticsearch_dsl.Search): search results
        remove_keys: tuple

    Returns:
        list of dicts: query results.
    """
    output = []
    for ele in response:
        data = ele.to_dict()
        if remove_keys:
            data = {k: v for k, v in data.items() if k not in remove_keys}
        data['id'] = ele.meta.id
        output.append(data)
    return output
