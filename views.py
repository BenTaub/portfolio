from django.http import HttpResponseRedirect
from django.shortcuts import render

from balancer.forms import ManageSecurity
from balancer.models import SecuritiesAvail


# Create your views here.
def manage_a_security(request):
    """Add a new or manage an existing security"""

    if 'id' not in request.GET:  # This is a request relating to a security that's not in the DB yet
        if request.method == 'GET':  # This is a request to show a blank entry form_contact
            return render(request, template_name='manage_security.html',
                          context={'security_details_form': ManageSecurity()})
        else:  # The user has entered data and this is a request to put it into the DB
            security_details_form = ManageSecurity(request.POST)
            if security_details_form.has_changed():
                # There actually was data typed into the blank form_contact, put it into the DB
                if security_details_form.is_valid():
                    # Save the data in the DB & then redisplay it, with an ID
                    new_security = SecuritiesAvail(
                        name=security_details_form.data['name'], symbol=security_details_form.data['symbol'],
                        price=security_details_form.data['price'])
                    new_security.save()
                    return HttpResponseRedirect(redirect_to='/balancer/security_manage/?id=' +
                                                            str(new_security.id))
                else:
                    # Form data wasn't valid - show form & errors to the user
                    return render(request, template_name='manage_security.html',
                                  context={'security_details_form': security_details_form})

    # This is a request relating to a security that is already in the DB
    # Read the existing record
    qry_filters = {'id': request.GET['id'], 'current_rec_fg': True}
    security_data = SecuritiesAvail.objects.get(**qry_filters)
    security_details_form = ManageSecurity(security_data.__dict__)

    # Is this a request to show an existing record?
    if request.method == 'GET':
        return render(request, template_name='manage_security.html',
                      context={'security_details_form': security_details_form})

    # Is this a request to delete the record?
    if request.POST.get("delete"):
        # TODO: Put in some 'are you sure?' code
        security_data.delete()
        return HttpResponseRedirect(redirect_to='/balancer/security_manage/')

    return render(request, template_name='manage_security.html', context={'security_details_form': ManageSecurity()})


def maint_avail_securities(request):
    """Show a list of available securities"""
    return render(request, template_name='avail_securities.html', context={})
