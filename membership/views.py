from django.shortcuts import render,redirect,get_object_or_404
from .models import MembershipCategory
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import MembershipRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import MembershipRegistration
from pyisemail import is_email
import pycountry




# Create your views here.
class membershipCategory(ListView):
    model = MembershipCategory
    template_name = 'membership/member_cat.html'
    context_object_name = 'categories'


def is_student_email(email):
    if is_email(email, check_dns=True, diagnose=True):
        domain = email.split('@')[1]
        country_codes = [country.alpha_2 for country in pycountry.countries]
        if domain.endswith('.edu') or domain.endswith('.ac') or domain.endswith('.students') or any(domain.endswith('.' + code.lower()) for code in country_codes):
            return True
    return False



def membership_registration(request, category_id):
    category = get_object_or_404(MembershipCategory, id=category_id)
    user = request.user
    try:
        membership = MembershipRegistration.objects.get(user=user)
        initial_data = {
            'membership': category.title,
            'membership_price': category.price
        }
        form = MembershipRegistrationForm(request.POST or None, instance=membership, initial=initial_data)
    except MembershipRegistration.DoesNotExist:
        initial_data = {
            'membership': category.title,
            'membership_price': category.price,
            'user': user,
        }
        form = MembershipRegistrationForm(request.POST or None, initial=initial_data)
        
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            
            # Validate student email for "Students/Post-doctoral/Early career scientists" category
            if category.title == 'Students/Post-doctoral/Early career scientists':
                email = form.cleaned_data.get('email')
                if not is_student_email(email):
                    form.add_error('email', 'Invalid student email')
                    return render(request, 'membership/member_reg.html', {'form': form, 'category': category})
            
            instance.save()
            messages.success(request, 'Membership registration details updated successfully')
            return redirect('membership:payment_method')
        
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'membership/member_reg.html', context)





def payment_method(request):
    user_id = request.user.id
    try:
        membership_registration = MembershipRegistration.objects.get(user_id=user_id)
        # retrieve the necessary information from the membership_registration object
        context = {
            'membership': membership_registration
        }
        return render(request, 'membership/payment_method.html', context)
    except MembershipRegistration.DoesNotExist:
        return redirect('membership:member_reg')