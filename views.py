import datetime

from django.db import IntegrityError
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render

from balancer.forms import FormManageSecurity, FormAddSecurity, FormSetSecurities, FormSetSecurityPrices, \
    FormAccount, FormAccountHolding
from balancer.models import Security, SecurityPrice, store_formset_in_db, dictfetchall, Account, Holding


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


def set_security_prices(request, date):
    """Present the user with a list of prices"""
    qry = ('SELECT balancer_security.id AS security_id, balancer_security.name, balancer_security.symbol, '
           'balancer_securityprice.id, %s AS price_dt, balancer_securityprice.price, balancer_securityprice.notes '
           # 'balancer_securityprice.price_dt, balancer_securityprice.price, balancer_securityprice.notes, %s AS DATE '
           'FROM balancer_security LEFT OUTER JOIN balancer_securityprice '
           'ON (balancer_security.id = balancer_securityprice.security_id '
           'AND balancer_securityprice.price_dt=%s) '
           'ORDER BY balancer_security.name')
    cursor = connection.cursor()
    cursor.execute(qry, [date, date])

    security_price_recs = dictfetchall(cursor=cursor)
    security_prices_formset = FormSetSecurityPrices(initial=security_price_recs)

    if request.method == 'GET':  # request to set up basic price data
        return render(request, template_name='set_security_prices.html',
                      context={'price_date': date, 'price_formset': security_prices_formset})

    # This isn't a GET so it must have been a POST
    security_prices_formset = FormSetSecurityPrices(request.POST, initial=security_price_recs)
    if security_prices_formset.is_valid():
        store_formset_in_db(formset=security_prices_formset, db_model=SecurityPrice)
    else:
        return render(request, template_name='set_security_prices.html',
                      context={'price_date': date, 'price_formset': security_prices_formset})

    return render(request, template_name='home.html')


def set_price_date(request):
    """Allows user to set the date for security price entries"""
    if request.method == 'POST':
        date = request.POST['date']
        return HttpResponseRedirect(redirect_to='/balancer/set_security_prices/' + date)
    return render(request, template_name='set_a_date.html',
                  context={'heading': "Set A Price Date", 'date': datetime.date.today()})


def maint_accts(request, acct_id):
    """Allows user to maintain their investment accounts"""
    if acct_id != '':
        # TODO: Crashes if acct_id is not found. Do I need to test for this? How could it happen?
        db_rec = Account.objects.get(id=acct_id)

    if request.method == 'GET':
        if acct_id == '':  # Request to enter a new account
            return render(request, template_name='manage_account.html', context={'form_acct': FormAccount()})
        else:
            form_acct = FormAccount(instance=db_rec)
            return render(request, template_name='manage_account.html', context={'form_acct': form_acct})

    # Not a GET so must be a POST
    if acct_id != '':
        form_acct = FormAccount(request.POST, instance=db_rec)
    else:
        form_acct = FormAccount(request.POST)

    if form_acct.is_valid():
        form_acct.save()
        return HttpResponseRedirect(redirect_to='/balancer/acct/' + str(form_acct.instance.id))
    else:
        return render(request, template_name='manage_account.html',
                      context={'form_acct': form_acct, 'instance': None})


def add_holding_to_acct(request, holding_id):
    """Allows user to add a holding to a particular account"""
    # TODO: Add support for previous & next buttons
    db_rec = None
    if holding_id != '':
        db_rec = Holding.objects.get(id=holding_id)
        # TODO: We should include some sort of indicator on the screen when you're at the first or last item
        if 'previous' in request.POST:
            prev_rec = (Holding.objects
                        .filter(asset=db_rec.asset, account=db_rec.account, as_of_dt__lt=db_rec.as_of_dt)
                        .order_by('-as_of_dt'))
            if len(prev_rec) > 0:
                return HttpResponseRedirect(redirect_to='/balancer/acct/holding/' + str(prev_rec[0].id))
        elif 'next' in request.POST:
            next_rec = (Holding.objects
                        .filter(asset=db_rec.asset, account=db_rec.account, as_of_dt__gt=db_rec.as_of_dt)
                        .order_by('as_of_dt'))
            if len(next_rec) > 0:
                return HttpResponseRedirect(redirect_to='/balancer/acct/holding/' + str(next_rec[0].id))

    if request.method == 'GET':
        if holding_id == '':  # Request to add a new holding
            return render(request, template_name='add_holding_to_acct.html',
                          context={'form': FormAccountHolding()})
        else:
            form_assignment = FormAccountHolding(instance=db_rec, new_holding=False)
            return render(request, template_name='add_holding_to_acct.html', context={'form': form_assignment})

    # Not a GET so must be a POST
    if 'new' in request.POST:
        return HttpResponseRedirect(redirect_to='/balancer/acct/holding')

    if holding_id == '':  # This is a new holding rec
        form_assignment = FormAccountHolding(request.POST, new_holding=True)
    else:
        if 'delete' in request.POST:
            Holding.objects.filter(id=holding_id).delete()
            # TODO: Change this redirect to go back to the list of all holdings
            return HttpResponseRedirect(redirect_to='/balancer')
        form_assignment = FormAccountHolding(request.POST, instance=db_rec, new_holding=False)
    if form_assignment.is_valid():
        form_assignment.save()
        return HttpResponseRedirect(redirect_to='/balancer/acct/holding/' + str(form_assignment.instance.id))
    else:
        return render(request, template_name='add_holding_to_acct.html',
                      context={'form': form_assignment})
