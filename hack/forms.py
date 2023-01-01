from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Register")

class EditUserForm(FlaskForm):
    username = StringField('Updated text', validators=[DataRequired()])
    email = StringField('Updated text2', validators=[DataRequired()])
    points = IntegerField('Points')
    submit = SubmitField('Submit')

class StudentForm(FlaskForm):
    g1 = IntegerField('G1')
    g2 = IntegerField('G2')
    studytime = IntegerField('Study time')
    failures = IntegerField('Failures')
    absences = IntegerField('Absences')
    freetime = IntegerField('Freetime')
    submit = SubmitField('Submit')
