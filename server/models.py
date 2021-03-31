from elasticsearch_dsl import (
    Document,
    SearchAsYouType,
    Text,
    analyzer,
    token_filter,
    Keyword,
    tokenizer
)
from elasticsearch_dsl.query import MultiMatch
from .utils import build_elastic_results_dict


ascii_fold = analyzer(
    "ascii_fold",
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)

custom_analyzer = analyzer('custom_analyzer',
    tokenizer=tokenizer('ngram', min_gram=3, max_gram=5),
    filter=['lowercase']
)

email_analyzer = analyzer('email',
    tokenizer=tokenizer('uax_url_email'),
    filter=['trim', 'lowercase']
)


class SamVendors(Document):
    duns = Keyword()
    duns_plus_four = Keyword()
    cage_code = Text(fields={'raw': Keyword()})
    legal_business_name = SearchAsYouType(max_shingle_size=3, analyzer=ascii_fold)
    elec_govt_bus_poc_email = Text(fields={'raw': Keyword()}, analyzer=email_analyzer)
    full_address = SearchAsYouType(max_shingle_size=3, analyzer=ascii_fold)
    mailing_address_line1 = Text(fields={'raw': Keyword()}, analyzer=custom_analyzer)
    mailing_address_line2 = Text(fields={'raw': Keyword()}, analyzer=custom_analyzer)
    mailing_address_city = Text(fields={'raw': Keyword()}, analyzer=custom_analyzer)
    mailing_address_state = Text(fields={'raw': Keyword()}, analyzer=custom_analyzer)
    mailing_address_zip = Text(fields={'raw': Keyword()})
    mailing_address_zip_plus_four = Text(fields={'raw': Keyword()})
    mailing_address_country = Keyword()

    class Index:
        name = "vendors"
        settings = {"number_of_shards": 10, "number_of_replicas": 0}

    def auto_complete(self, query, field, size=15):
        """Do search as to type on field

        Args:
            query (str): query string
            field (str): attribute name, e.g. legal_business_name
            size (int, optional): Search size. Defaults to 15.

        Returns:
            [type]: [description]
        """
        assert hasattr(self, field), f"{self.__class__.__name__} has no attribute {field}"

        search = self.search()
        search.query = MultiMatch(
            query=query,
            type="bool_prefix",
            fields=[
                f"{field}",
                f"{field}._2gram",
                f"{field}._3gram"
            ],
        )
        search = search.extra(size=size)
        response = search.execute()
        return build_elastic_results_dict(response)

