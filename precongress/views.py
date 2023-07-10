from django.shortcuts import *
from .models import *
from django.views.generic import *
from .forms import PrecongressRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
# from .models import MembershipRegistration
from pyisemail import is_email
import pycountry
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# Create your views here.
class precongressCategory(ListView):
    model = PrecongressCategory
    template_name = 'precongress/precongress_cat.html'
    context_object_name = 'categories'



def is_student_email(email):
    if is_email(email, check_dns=True, diagnose=True):
        domain = email.split('@')[1]
        country_codes = [country.alpha_2 for country in pycountry.countries]
        if domain.endswith('.edu') or domain.endswith('.ac') or domain.endswith('.students') or any(domain.endswith('.' + code.lower()) for code in country_codes):
            return True
    return False


def membership_registration(request, category_id):
    category = get_object_or_404(PrecongressCategory, id=category_id) 
    user = request.user
    try:
        registration = PrecongressRegistration.objects.get(user=user)
        initial_data = {
            'membership': category.title,
            'precongress_price': category.price 
        }
        form = PrecongressRegistrationForm(request.POST or None, instance=registration, initial=initial_data)  # Use PrecongressRegistrationForm instead of MembershipRegistrationForm
    except PrecongressRegistration.DoesNotExist:
        initial_data = {
            'membership': category.title,
            'precongress_price': category.price,  # Use precongress_price instead of membership_price
            'user': user,
        }
        form = PrecongressRegistrationForm(request.POST or None, initial=initial_data)  # Use PrecongressRegistrationForm instead of MembershipRegistrationForm

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
            messages.success(request, 'Precongress registration details updated successfully')  # Update success message
            return redirect('membership:payment_method')

    context = {
        'form': form,
        'category': category
    }
    return render(request, 'precongress/member_reg.html', context)


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def precongress_users(request):
    registrations = PrecongressRegistration.objects.all()

    paginator = Paginator(registrations, 10)  # Display 10 registrations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'precongress/manage.html', {'page_obj': page_obj})