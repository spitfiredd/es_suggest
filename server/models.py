from elasticsearch_dsl import Document, SearchAsYouType, Text, analyzer, token_filter, Keyword, tokenizer


ascii_fold = analyzer(
    "ascii_fold",
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)

custom_analyzer = analyzer('custom_analyzer',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=3, max_gram=3),
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
