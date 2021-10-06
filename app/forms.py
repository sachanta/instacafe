from flask_wtf import FlaskForm
#from flask.ext.wtf import Form
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Required


class TipsForm(FlaskForm):
    from_date = DateField('From_Date', validators=[DataRequired()])
    to_date = DateField('To_Date', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')