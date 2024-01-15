from django.shortcuts import render, HttpResponse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django_htmx.http import trigger_client_event

from .forms import CarrierForm
from core.models import SlotTime, Vehicle

# Create your views here.
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
        context = {'form': CarrierForm()}
        return render(request, 'add_carrier.html', context)
    elif request.method == 'POST':
        form = CarrierForm(request.POST)
        if form.is_valid():
            carrier = form.save()
            message = f'{carrier.carrier} added successfully!'
            context = {'form': CarrierForm(), 'message': message}
            return render(request, 'add_carrier.html#carrier-form', context)
        
        context = {'form': form}
        return render(request, 'add_carrier.html#carrier-form', context)
