from flask_wtf import FlaskForm 
from wtforms import SelectField, StringField, PasswordField, IntegerField, SubmitField 
from wtforms.validators import InputRequired, EqualTo

class CountyForm(FlaskForm):
    
    c_county=SelectField("County:", choices=["Galway", "Leitrim", "Mayo", "Roscommon", "Sligo", "Antrim", "Armagh", "Cavan", "Donegal", "Down", "Fermanagh", "Derry", "Monaghan", "Tyrone", "Clare", "Cork", "Kerry", "Limerick", "Tipperary", "Waterford", "Carlow", "Dublin", "Kildare", "Kilkenny", "Laois", "Longford", "Louth", "Meath", "Offaly", "Westmeath", "Wexford", "Wicklow"], validators=[InputRequired()])
    streak=IntegerField("Streak:")
    submit=SubmitField("Submit")

class SignForm(FlaskForm):
    username=StringField("Please enter a username:", validators=[InputRequired()] )
    password=PasswordField("Please enter a password:", validators=[InputRequired()])
    password_again=PasswordField("Confirm password:", validators=[InputRequired(), EqualTo("password")])
    submit=SubmitField("Submit")   
class LoginForm(FlaskForm):
    username=StringField("Please enter username:", validators=[InputRequired()] )
    password=PasswordField("Please enter password:", validators=[InputRequired()])
    submit=SubmitField("Submit")  
class CommentForm(FlaskForm)   :
    comment=StringField("Comment:", validators=[InputRequired()])
    submit=SubmitField("Submit")