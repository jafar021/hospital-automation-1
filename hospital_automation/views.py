from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
from datetime import datetime
from hospital_automation.serializers import PatientSerializer
from django.shortcuts import render, redirect
from django.conf.urls import *
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

counter = 1


@login_required
def doctors(request):
    user_group = request.user.groups.values_list('name', flat=True)[0]
    if user_group == 'Doctor':
        patient = list(Patient.objects.values().filter(is_seen=False))
        print(patient)
        return render(request, 'incoming_patient.html', {'incoming_patient': patient})
    else:
        return render(request, 'index.html', {'user_group': 'Doctor'})


def receive_patient(request):
    global counter
    print(counter)
    if request.method == 'GET' and counter == 0:
        incoming_patient = list(Patient.objects.values().filter(
            is_seen=False).order_by('-id')[:1])
        serializer = PatientSerializer(
            incoming_patient, many=True, context={'request': request})
        counter = 1
        print(incoming_patient)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)


@login_required
def reception(request):
    user_group = request.user.groups.values_list('name', flat=True)[0]
    if(user_group == 'Receptionist'):
        global counter
        if request.method == 'GET':
            return render(request, 'reception.html', {})
        elif request.method == 'POST':
            first_name = request.POST['First Name']
            last_name = request.POST['Last Name']
            father_name = request.POST['Father name']
            address = request.POST['Address']
            city = request.POST['City']
            state = request.POST['State']
            zip_code = request.POST['Postal/ZIP code']
            country = request.POST['Country']
            country_code = request.POST['country code']
            contact_number = request.POST['Contact Number']
            date = request.POST['todays date']
            problem = request.POST['problem']
            alloted_doctor = request.POST['Doctor name']
            Patient.objects.create(first_name=first_name, last_name=last_name, guardian_name=father_name, address=address,
                                   city=city, state=state, zip_code=zip_code, country=country,
                                   country_code=country_code, phone_number=contact_number, date=date, problem_name=problem, assigned_doctor=alloted_doctor)
            counter = 0
            return redirect('reception')
    else:
        return render(request, 'index.html', {'user_group': 'Receptionist'})


@csrf_exempt
def autocomplete(request, id):
    if request.is_ajax():
        queryset = User_type.objects.filter(
            specialization__startswith=request.GET['search'])
        list = []
        for problem in queryset:
            if problem.specialization not in list:
                list.append(problem.specialization)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'reception.html', {})


def prescriptions(request, patient_id):
    patient_prescriptions = list(
        Patient_history.objects.values().filter(user_id=patient_id))
    print(patient_prescriptions)
    return render(request, 'patient_prescriptions.html', {'prescriptions': patient_prescriptions})


def load_doctors(request):
    if request.is_ajax():
        problem = request.GET.get('problem')
        doctor_id = User_type.objects.values(
            'user_id').filter(specialization=problem)
        doctors = User.objects.values(
            'first_name', 'last_name').filter(id__in=doctor_id)
        list = []
        for doctor in doctors:

            list.append(doctor['first_name'] + " " + doctor['last_name'])

        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'reception.html', {})


def index(request):
    return render(request, 'index.html', {})
