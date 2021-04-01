from .extensions import db


class SamVendors(db.Model):

    __tablename__ = 'sam_vendors'

    id = db.Column(db.Integer, primary_key=True)
    duns = db.Column(db.Text)
    duns_plus_four = db.Column(db.Text)
    cage_code = db.Column(db.Text)
    legal_business_name = db.Column(db.Text)
    elec_govt_bus_poc_email = db.Column(db.Text)
    mailing_address_line1 = db.Column(db.Text)
    mailing_address_line2 = db.Column(db.Text)
    mailing_address_city = db.Column(db.Text)
    mailing_address_state = db.Column(db.Text)
    mailing_address_zip = db.Column(db.Text)
    mailing_address_zip_plus_four = db.Column(db.Text)
    mailing_address_country = db.Column(db.Text)
