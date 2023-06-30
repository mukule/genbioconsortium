from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import PrecongressRegistration
from users.models import CustomUser

class PrecongressRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='First Name')
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Last Name')
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    membership = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label='Precongress Type')  # Update field name to "precongress"
    institution = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Institution')
    city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='City')
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
        label='Country',
    )
    occupation = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Occupation')
    terms_checkbox = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='I agree to the terms and conditions', error_messages={'required': 'You must agree to the terms and conditions'})
    precongress_price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), label='Precongress Price')  # Update field name to "precongress_price"
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PrecongressRegistration  # Update the model to PrecongressRegistration
        fields = ['first_name', 'last_name', 'email', 'membership', 'institution', 'city', 'country', 'occupation', 'terms_checkbox', 'precongress_price', 'user']  # Update field name to "precongress"
        widgets = {'terms_checkbox': forms.CheckboxInput(attrs={'required': True})}  # Update widget name to "terms_checkbox"
