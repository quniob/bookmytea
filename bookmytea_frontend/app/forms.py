from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, ValidationError


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired(), Email()], render_kw={"placeholder": "Почта"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Пароль"})
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired()], render_kw={"placeholder": "Подтверждение пароля"})
    submit = SubmitField('Регистрация')

    def validate_confirm_password(self, field):
        if self.password.data != field.data:
            raise ValidationError('Пароли не совпадают!')
