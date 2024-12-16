from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

class NewInstrument(FlaskForm):
    date_bought = DateField('Date Bought', format='%Y-%m-%d', validators=[DataRequired()])
    nickname = StringField("Nickname", validators=[DataRequired()])
    year = IntegerField("Year")
    maker = StringField("Maker")
    type = SelectField('Type', choices=[
        ('other', 'Other'),
        ('string', 'String'),
        ('woodwind', 'Woodwind'),
        ('brass', 'Brass'),
        ('percussion', 'Percussion')
    ])
    used = BooleanField("Used")
    submit = SubmitField("Submit")
