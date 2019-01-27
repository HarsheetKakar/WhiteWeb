from flask_wtf import FlaskForm as Form
from wtforms import TextField, PasswordField, SubmitField
#from wtforms.validators import InputRequired, EqualTo, Length, Email

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username'
    )
    email = TextField(
        'Email'
    )
    password = PasswordField(
        'Password'
    )
    submit = SubmitField(
        label="Submit",
        )#submit button added


class LoginForm(Form):
    name = TextField('Username', )
    password = PasswordField('Password',)
    submit = SubmitField(label="Submit") #submit button added
