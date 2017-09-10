from django.http import HttpResponseRedirect
from django.shortcuts import render

from balancer.forms import ManageSecurity
from balancer.models import SecurityAvail


# Create your views here.
def manage_a_security(request):
    """Add a new or manage an existing security"""

    if 'security_avail_static' not in request.GET:  # This is a request relating to a security that's not in the DB yet
        if request.method == 'GET':  # This is a request to show a blank entry form_contact
            return render(request, template_name='manage_security.html',
                          context={'security_details_form': ManageSecurity()})
        else:  # The user has entered data and this is a request to put it into the DB
            security_details_form = ManageSecurity(request.POST)
            if security_details_form.has_changed():
                # There actually was data typed into the blank form_contact, put it into the DB
                if security_details_form.is_valid():
                    # Save the data in the DB & then redisplay it, with an ID
                    new_security = SecurityAvail(
                        name=security_details_form.data['name'], symbol=security_details_form.data['symbol'],
                        price=security_details_form.data['price'])
                    new_security.create()
                    return HttpResponseRedirect(redirect_to='/balancer/security_manage/?security_avail_static=' +
                                                            str(new_security.security_avail_static.id))
                else:
                    # Form data wasn't valid - show form & errors to the user
                    return render(request, template_name='manage_security.html',
                                  context={'security_details_form': security_details_form})

    # This is a request relating to a security that is already in the DB
    # Read the existing record from the DB
    qry_filters = {'security_avail_static': request.GET['security_avail_static'], 'current_rec_fg': True}
    old_security_data = SecurityAvail.objects.get(**qry_filters)
    old_security_details_form = ManageSecurity(old_security_data.__dict__)
    new_security_details_form = ManageSecurity(request.POST, initial=old_security_data.__dict__)

    # Is this a request to show an existing record?
    if request.method == 'GET':
        return render(request, template_name='manage_security.html',
                      context={'security_details_form': old_security_details_form})

    # Is this a request to delete the record?
    if request.POST.get("delete"):
        # TODO: Put in some 'are you sure?' code
        old_security_data.delete()
        # TODO: Change this to redirect to the securities list page when it's written
        return HttpResponseRedirect(redirect_to='/balancer/security_manage/')

    # TODO: start here!!!!
    if request.POST.get("save"):
        if new_security_details_form.has_changed():
            if new_security_details_form.is_valid():
                # Save the data in the DB & then redisplay it, with an ID
                new_security = SecurityAvail(
                    id=new_security_details_form.data['id'],
                    name=new_security_details_form.data['name'], symbol=new_security_details_form.data['symbol'],
                    price=new_security_details_form.data['price'],
                    effective_dt=new_security_details_form.data['at_dt'])
                new_security.update()
                return HttpResponseRedirect(redirect_to='/balancer/security_manage/?id=' +
                                                        str(new_security.id))

    return render(request, template_name='manage_security.html', context={'security_details_form': ManageSecurity()})


def maint_avail_securities(request):
    """Show a list of available securities"""
    return render(request, template_name='avail_securities.html', context={})
