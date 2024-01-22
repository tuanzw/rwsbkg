from django.shortcuts import render, HttpResponse, get_object_or_404
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

import json

from .forms import CarrierForm, UserForm, UserUpdateForm, SetUserPasswordForm
from core.models import SlotTime, Vehicle, Carrier, User


def home(request):
    slots = SlotTime.objects.all()
    vehicles = Vehicle.objects.all()
    if request.htmx:
        return render(request, 'partial.html', {})
    else:
        context = {'slots':slots, 'vehicles':vehicles}
        return render(request, 'home.html', context)
    

def add_carrier(request):
    if not request.htmx:
        carriers = Carrier.objects.all()
        context = {'carriers': carriers}
        return render(request, 'carrier.html', context)
    else:
        if request.method == 'GET':
            context = {'form': CarrierForm()}
            return render(request, 'carrier.html#carrier-form', context)
        elif request.method == 'POST':
            form = CarrierForm(request.POST)
            if form.is_valid():
                carrier = form.save()
                message = f'{carrier.carrier} added successfully!'
                context = {'carriers': [carrier],}
                response = render(request, 'carrier.html#carrier-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'carrier.html#carrier-form', context)


def list_carrier(request):
    if request.method == 'GET':
        carriers = Carrier.objects.all()
        context = {'carriers': carriers}
        return render(request, 'carrier.html#carrier-rows', context)


def edit_carrier(request, id):
    if request.method == 'GET':
        carrier = get_object_or_404(Carrier, pk=id)
        carrier_frm = CarrierForm(instance=carrier)
        context = {'form': carrier_frm}
        return render(request, 'carrier.html#carrier-form', context)
    elif request.method == 'POST':
        print(request.POST)
        carrier = get_object_or_404(Carrier, pk=id)
        form = CarrierForm(request.POST, instance=carrier)
        if form.is_valid():
            carrier = form.save()
            context = {'carrier': carrier}
            message = f'{carrier.carrier} updated successfully!'
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
        return render(request, 'carrier.html#carrier-form', context)
        


def check_carrier(request):
    carrier_frm = CarrierForm(request.GET)
    response = HttpResponse(as_crispy_field(carrier_frm['carrier']))
    if carrier_frm.has_error('carrier'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')
    
    

def delete_carrier(request, id):
    if request.method == 'DELETE':
        carrier = Carrier.objects.filter(pk=id).first()
        carrier.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'on-success': None,
                'showMessage': f'Carrier {carrier.carrier} deleted!',
            })
        })
        

def list_user(request):
    if request.method == 'GET':
        users = User.objects.all().select_related('carrier')
        context = {'users': users}
        return render(request, 'user.html#user-rows', context)
     
def add_user(request):
    if not request.htmx:
        users = User.objects.all().select_related('carrier')
        context = {'users': users}
        return render(request, 'user.html', context)
    else:
        if request.method == 'GET':
            context = {'form': UserForm()}
            return render(request, 'user.html#user-form', context)
        elif request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                message = f'{user.username} added successfully!'
                context = {'users': [user],}
                response = render(request, 'user.html#user-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'user.html#user-form', context)

def edit_user(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=id)
        user_frm = UserUpdateForm(instance=user)
        context = {'form': user_frm}
        return render(request, 'user.html#user-form', context)
    elif request.method == 'POST':
        print(request.POST)
        user = get_object_or_404(User, pk=id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            context = {'user': user}
            message = f'{user.username} updated successfully!'
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
        return render(request, 'user.html#user-form', context)
def delete_user(request, id):
    if request.method == 'DELETE':
        user = User.objects.filter(pk=id).first()
        user.delete()
        return HttpResponse(status=200, headers={
            'HX-Trigger': json.dumps({
                'showMessage': f'User {user.username} deleted!',
            })
        })
def check_username(request):
    user_frm = UserForm(request.GET)
    response = HttpResponse(as_crispy_field(user_frm['username']))
    if user_frm.has_error('username'):
        return trigger_client_event(response, 'frm-has-errors')
    return trigger_client_event(response, 'frm-no-errors')

def set_password(request, id):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=id)
        user_frm = SetUserPasswordForm(instance=user)
        print(user)
        context = {'form': user_frm}
        return render(request, 'user.html#user-form', context)
    elif request.method == 'POST':
        print(request.POST)
        user = get_object_or_404(User, pk=id)
        form = SetUserPasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            context = {'user': user}
            message = f'Password for {user.username} changed successfully!'
            response = HttpResponse(status=200, headers={
                'HX-Trigger': json.dumps({
                    'on-success': None,
                    'showMessage': message
                })
            })
            print(response.headers)
            return response
        print(form.errors)
        context = {'form': form}
        return render(request, 'user.html#user-form', context)