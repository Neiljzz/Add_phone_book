from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    EmailField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


class PhoneForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class AddressForm(FlaskForm):
    street_name = StringField('Street Name', validators=[InputRequired()])
    number = IntegerField("Number", validators=[InputRequired()])
    unit = StringField("Unit")
    postal_code = StringField("Postal code", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])
    
    submit = SubmitField('Create')


class SearchForm(FlaskForm):
    search_term = StringField('Search Term')
    submit = SubmitField('Search')