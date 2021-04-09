from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UpdateByCageForm(FlaskForm):
    cage = StringField('cage', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
