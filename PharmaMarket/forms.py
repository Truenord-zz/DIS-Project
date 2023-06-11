from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from PharmaMarket.queries import get_user_by_user_name, get_pharmacist_by_pk, get_customer_by_pk
from PharmaMarket.utils.choices import DrugIdChoices, DrugNameChoices, UserTypeChoices, \
    DrugCityChoices, DrugBrandChoices


class UserLoginForm(FlaskForm):
    user_name = StringField('Username',
                    validators=[DataRequired(), Length(min=2, max=50)],
                    render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                    validators=[DataRequired()],
                    render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user is None:
            raise ValidationError(f'User name "{self.user_name.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    full_name = StringField('Full name',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Full name'))
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                            validators=[DataRequired()],
                            render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                            validators=[DataRequired()],
                            render_kw=dict(placeholder='Password'))
    user_type = SelectField('User type',
                            validators=[DataRequired()],
                            choices=UserTypeChoices.choices())
    submit = SubmitField('Sign up')

    def validate_user_name(self, field):
        user = get_user_by_user_name(self.user_name.data)
        if user:
            raise ValidationError(f'User name "{self.user_name.data}" already in use.')

    def validate_password_repeat(self, field):
        if not self.password.data == self.password_repeat.data:
            raise ValidationError(f'Provided passwords do not match.')


class FilterDrugForm(FlaskForm):
    name = SelectField('Name',
                    choices=DrugNameChoices.choices())
    brand = SelectField('Brand',
                    choices=DrugBrandChoices.choices())
    city = SelectField('City',
                    choices=DrugCityChoices.choices())
    sold_by = StringField('Sold by')
    price = FloatField('Price (lower than or equal to)',
                    validators=[NumberRange(min=0, max=1000)])
    submit = SubmitField('Filter')

class AddDrugForm(FlaskForm):
    id = IntegerField('Id',
                    validators=[DataRequired(),
                    NumberRange(min=0, max=3000)])
    name = SelectField('Name (Subcategory)',
                    validators=[DataRequired()],
                    choices=DrugNameChoices.choices())
    price = IntegerField('Price',
                    validators=[DataRequired(),
                    NumberRange(min=0, max=1000)])
    city = SelectField('City',
                    validators=[DataRequired()],
                    choices=DrugCityChoices.choices())
    brand = SelectField('Brand',
                    validators=[DataRequired()],
                    choices=DrugBrandChoices.choices())
    pharmacist_pk = IntegerField('Pharmacist',
                    validators=[DataRequired()],
                    render_kw=dict(disabled='disabled'))
    submit = SubmitField('Add drug')

    def validate_price(self, field):
        pharmacist = get_pharmacist_by_pk(self.pharmacist_pk.data)
        if pharmacist is None:
            raise ValidationError("You need to be a pharmacist to sell drugs!")


class BuyDrugForm(FlaskForm):
    submit = SubmitField('Yes, buy it')

    def validate_submit(self, field):
        customer = get_customer_by_pk(current_user.pk)
        if not customer:
            raise ValidationError("You must be a customer in order to create orders.")


class RestockDrugForm(FlaskForm):
    submit = SubmitField('Yes, restock it')
