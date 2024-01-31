from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from ..forms import DriverForm
from core.models import Driver

@login_required()
def list_driver(request):
    if request.method == 'GET':
        if not (request.user.is_superuser and request.user.is_staff):
            drivers = Driver.objects.filter(carrier=request.user.carrier).select_related('carrier')
        else:
            drivers = Driver.objects.all().select_related('carrier')
        context = {'drivers': drivers}
        return render(request, 'driver.html#driver-rows', context)

@login_required
def add_driver(request):
    if not request.htmx:
        if not (request.user.is_superuser and request.user.is_staff):
            drivers = Driver.objects.filter(carrier=request.user.carrier).select_related('carrier')
        else:
            drivers = Driver.objects.all().select_related('carrier')

        context = {'drivers': drivers}
        return render(request, 'driver.html', context)
    else:
        if request.method == 'GET':
            context = {'form': DriverForm(user=request.user)}
            return render(request, 'driver.html#driver-form', context)
        elif request.method == 'POST':
            form = DriverForm(request.POST, user=request.user)
            if form.is_valid():
                driver = form.save()
                message = f'{driver.fullname} added successfully!'
                context = {'drivers': [driver],}
                response = render(request, 'driver.html#driver-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'driver.html#driver-form', context)

@login_required
def edit_driver(request, id):
    if request.method == 'GET':
        driver = get_object_or_404(Driver, pk=id)
        driver_frm = DriverForm(instance=driver, user=request.user)
        context = {'form': driver_frm}
        return render(request, 'driver.html#driver-form', context)
    elif request.method == 'POST':
        driver = get_object_or_404(Driver, pk=id)
        form = DriverForm(request.POST, instance=driver, user=request.user)
        if form.is_valid():
            driver = form.save()
            context = {'driver': driver}
            message = f'{driver.fullname} updated successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'on-success': None,
                    'showMessage': message
                })
            })
            print(response.headers)
            return response
        print(form.errors)
        context = {'form': form}
        return render(request, 'driver.html#driver-form', context)

