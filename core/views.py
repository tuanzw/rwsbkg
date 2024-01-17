from django.shortcuts import render, HttpResponse
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import trigger_client_event

from .forms import CarrierForm
from core.models import SlotTime, Vehicle, Carrier


def home(request):
    slots = SlotTime.objects.all()
    vehicles = Vehicle.objects.all()
    if request.htmx:
        return render(request, 'partial.html', {})
    else:
        context = {'slots':slots, 'vehicles':vehicles}
        return render(request, 'home.html', context)
    

def add_carrier(request):
    if request.method == 'GET':
        carriers = Carrier.objects.all()
        context = {'form': CarrierForm(), 'carriers': carriers}
        return render(request, 'add_carrier.html', context)
    elif request.method == 'POST':
        form = CarrierForm(request.POST)
        if form.is_valid():
            carrier = form.save()
            message = f'{carrier.carrier} added successfully!'
            context = {'carrier': carrier, 'message': message}
            response = render(request, 'add_carrier.html#carrier-row', context)
            return trigger_client_event(response, 'showMessage', message)
         
        context = {'form': form}
        return render(request, 'add_carrier.html#carrier-form', context)
    
    
def check_carrier(request):
    carrier_frm = CarrierForm(request.GET)
    return HttpResponse(as_crispy_field(carrier_frm['carrier']))

def delete_carrier(request, id):
    if request.method == 'DELETE':
        Carrier.objects.filter(pk=id).delete()
        return HttpResponse(status=200) #Empty content
