from .extensions import db
from sqlalchemy.sql import func
import sqlalchemy as sa
from sqlalchemy.schema import DDL

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

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


trigger_function = DDL(
    "CREATE OR REPLACE FUNCTION modify_updated_at() "
    "RETURNS TRIGGER AS $$ "
    "BEGIN "
    "NEW.updated_at = now(); "
    "RETURN NEW; "
    "END; "
    "$$ language 'plpgsql';"
)

trigger = DDL(
    "CREATE TRIGGER updated_at_trigger BEFORE UPDATE "
    "ON sam_vendors FOR EACH ROW EXECUTE PROCEDURE "
    "modify_updated_at();"
)


sa.event.listen(
    SamVendors.__table__,
    'after_create',
    trigger_function
)


sa.event.listen(
    SamVendors.__table__,
    'after_create',
    trigger
)
