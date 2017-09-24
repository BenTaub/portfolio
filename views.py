import datetime

from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from balancer.forms import FormManageSecurity, FormAddSecurity, FormSetSecurities
from balancer.models import Security


# Create your views here.
def home(request):
    """Displays the home screen"""
    return render(request, template_name='home.html')


def manage_a_security(request):
    """Add a new or manage an existing security"""
    if 'id' not in request.GET:  # This is a request relating to a security that's not in the DB yet
        if request.method == 'GET':  # This is a request to show a blank entry form_contact
            return render(request, template_name='manage_security.html',
                          context={'form_security_details': FormAddSecurity()})
        else:  # The user has entered data and this is a request to put it into the DB
            form_security_details = FormAddSecurity(request.POST)
            if form_security_details.is_valid():
                # Save the data in the DB & then redisplay it, with an ID
                new_security = Security(
                    name=form_security_details.data['name'], symbol=form_security_details.data['symbol'],
                    notes=form_security_details.data['notes'])
                try:
                    new_security.save()
                except IntegrityError as err:
                    form_security_details.add_error(field='symbol', error="Symbol already used - try again")
                    return render(request, template_name='manage_security.html',
                                  context={'form_security_details': form_security_details})

                return HttpResponseRedirect(redirect_to='/balancer/securities_avail/')
            else:
                # Form data wasn't valid - show form & errors to the user
                return render(request, template_name='manage_security.html',
                              context={'form_security_details': form_security_details})

    # This is a request relating to a security that is already in the DB
    # Read the existing record from the DB
    qry_filters = {'id': request.GET['id']}
    old_security_data = Security.objects.get(**qry_filters)
    old_security_details_form = FormManageSecurity(old_security_data.__dict__)
    new_security_details_form = FormManageSecurity(request.POST, initial=old_security_data.__dict__)

    # Is this a request to show an existing record?
    if request.method == 'GET':
        return render(request, template_name='manage_security.html',
                      context={'form_security_details': old_security_details_form})

    if request.POST.get("save"):
        if new_security_details_form.has_changed():
            if new_security_details_form.is_valid():
                old_security_data.name = new_security_details_form.data['name']
                old_security_data.notes = new_security_details_form.data['notes']
                old_security_data.symbol = new_security_details_form.data['symbol']
                try:
                    old_security_data.save()
                except IntegrityError as err:
                    new_security_details_form.add_error(field='symbol', error="Symbol already used - try again")
                    return render(request, template_name='manage_security.html',
                                  context={'form_security_details': new_security_details_form})
                return HttpResponseRedirect(redirect_to='/balancer/securities_avail/')
        else:
            return HttpResponseRedirect(redirect_to='/balancer/securities_avail/')

    return HttpResponseRedirect(redirect_to='/balancer/securities_avail/')


def maint_avail_securities(request):
    """Show a list of available securities"""
    # Get all the records
    all_security_recs = Security.objects.order_by('name').values()
    all_securities_formset = FormSetSecurities(initial=all_security_recs)
    return render(request, template_name='avail_securities.html',
                  context={'formset': all_securities_formset})


def set_security_prices(request):
    """Present the user with a list of prices"""

    # TODO: Include a button with link to add a new security - how do you get back here, though?
    # TODO: Each security should link to the security price history page

    return render(request, template_name='set_security_prices.html',
                  context={'price_date': datetime.date.today(), 'price_formset': None})
