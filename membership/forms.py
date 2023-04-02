from django import forms
from django.contrib.auth.models import User
from .models import MembershipRegistration

class MembershipRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='First Name',
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Last Name',
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email',
    )
    membership = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label='Membership Type',
    )
    institution = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Institution',
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='City',
    )
    country = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Country',
    )
    occupation = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Occupation',
    )
    terms_checkbox = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the terms and conditions',
        error_messages={'required': 'You must agree to the terms and conditions'},
    )
    membership_price = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label='Membership Price',
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
        required=False,
    )

    

    class Meta:
        model = MembershipRegistration
        fields = ['first_name', 'last_name', 'email', 'membership', 'institution', 'city', 'country', 'occupation', 'terms_checkbox', 'membership_price', 'user']
        widgets = {'terms': forms.CheckboxInput(attrs={'required': True})}
