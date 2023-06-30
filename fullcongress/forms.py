from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import fullcongressRegistration
from users.models import CustomUser

class FullcongressRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='First Name')
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Last Name')
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    membership = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label='Full Congress Type')  # Update field name to "fullcongress"
    institution = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Institution')
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='City')
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
        label='Country',
    )
    occupation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Occupation')
    terms_checkbox = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='I agree to the terms and conditions', error_messages={'required': 'You must agree to the terms and conditions'})
    fullcongress_price = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label='Full Congress Price')  # Update field name to "fullcongress_price"
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = fullcongressRegistration
        fields = ['first_name', 'last_name', 'email', 'membership', 'institution', 'city', 'country', 'occupation', 'terms_checkbox', 'fullcongress_price', 'user']
        widgets = {'terms_checkbox': forms.CheckboxInput(attrs={'required': True})}
