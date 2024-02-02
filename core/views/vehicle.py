from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_htmx.http import trigger_client_event

import json

from ..forms import VehicleForm
from core.models import Vehicle

@login_required()
def list_vehicle(request):
    if request.method == 'GET':
        if not (request.user.is_superuser and request.user.is_staff):
            vehicles = Vehicle.objects.filter(carrier=request.user.carrier).select_related('carrier')
        else:
            vehicles = Vehicle.objects.all().select_related('carrier')
        context = {'vehicles': vehicles}
        return render(request, 'vehicle.html#vehicle-rows', context)

@login_required
def add_vehicle(request):
    if not request.htmx:
        if not (request.user.is_superuser and request.user.is_staff):
            vehicles = Vehicle.objects.filter(carrier=request.user.carrier).select_related('carrier')
        else:
            vehicles = Vehicle.objects.all().select_related('carrier')

        context = {'vehicles': vehicles}
        return render(request, 'vehicle.html', context)
    else:
        if request.method == 'GET':
            context = {'form': VehicleForm(user=request.user)}
            return render(request, 'vehicle.html#vehicle-form', context)
        elif request.method == 'POST':
            form = VehicleForm(request.POST, user=request.user)
            if form.is_valid():
                vehicle = form.save()
                message = f'{vehicle.registration_plate} added successfully!'
                context = {'vehicles': [vehicle],}
                response = render(request, 'vehicle.html#vehicle-rows', context)
                response = trigger_client_event(response, 'on-success')
                response = trigger_client_event(response, 'showMessage', message)
                return response
            
            context = {'form': form}
            return render(request, 'vehicle.html#vehicle-form', context)

@login_required
def edit_vehicle(request, id):
    if request.method == 'GET':
        vehicle = get_object_or_404(Vehicle, pk=id)
        vehicle_frm = VehicleForm(instance=vehicle, user=request.user)
        context = {'form': vehicle_frm}
        return render(request, 'vehicle.html#vehicle-form', context)
    elif request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=id)
        form = VehicleForm(request.POST, instance=vehicle, user=request.user)
        if form.is_valid():
            vehicle = form.save()
            context = {'vehicle': vehicle}
            message = f'{vehicle.registration_plate} updated successfully!'
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
        return render(request, 'vehicle.html#vehicle-form', context)
    

@login_required
def toggle_vehicle(request, id):
    if request.method == 'PATCH':
        vehicle = get_object_or_404(Vehicle, pk=id)
        if vehicle:
            vehicle.active = not vehicle.active
            vehicle.save()
            message = f'{vehicle.registration_plate} disabled successfully!'
            response = HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    'list-changed': None,
                    'showMessage': message
                })
            })
            return response



