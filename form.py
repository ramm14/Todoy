from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class todoForm(FlaskForm):
    todo_header = StringField("Header", validators=[DataRequired()])
    todo_description = StringField("Description", validators=[DataRequired()])
    todo_submit = SubmitField()
