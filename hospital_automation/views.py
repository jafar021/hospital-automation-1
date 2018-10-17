from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
from datetime import datetime,date
from hospital_automation.serializers import PatientSerializer
from django.shortcuts import render, redirect
from django.conf.urls import *
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
counter = 1
def doctors(request):
    patient = list(Patient.objects.values().filter(is_seen = False))
    return render(request,'incoming_patient.html', {'incoming_patient': patient})


def receive_patient(request):
    global counter
    print(counter)
    if request.method == 'GET' and counter == 0:
        incoming_patient = list(Patient.objects.values().filter(is_seen = False).order_by('-id')[:1])
        serializer = PatientSerializer(incoming_patient, many = True, context = {'request':request})
        counter = 1
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({}, safe = False)


def reception(request):
    global counter
    if request.method == 'GET':
        return render(request, 'reception.html', {})
    elif request.method == 'POST':
        first_name =  request.POST['First Name']
        last_name =  request.POST['Last Name']
        father_name =  request.POST['Father name']
        address =  request.POST['Address']
        city = request.POST['City']
        state = request.POST['State']
        zip_code = request.POST['Postal/ZIP code']
        country = request.POST['Country']
        country_code = request.POST['country code']
        contact_number = request.POST['Contact Number'] 
        date = request.POST['todays date']
        problem = request.POST['problem']
        alloted_doctor = request.POST['Doctor name']
        Patient.objects.create(first_name=first_name, last_name=last_name, guardian_name=father_name,
                                address=address, city=city, state=state, zip_code=zip_code, country=country, 
                                country_code=country_code, phone_number=contact_number, date=date,
                                problem_name=problem, assigned_doctor=alloted_doctor)
        counter = 0
        return redirect('reception')       

@csrf_exempt
def autocomplete(request, id):
    if request.is_ajax():
        queryset = User_type.objects.filter(specialization__startswith=request.GET['search'])
        list = []        
        for problem in queryset:
            if problem.specialization not in list:
                list.append(problem.specialization)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request,'reception.html',{})

def prescriptions(request,patient_id):
    patient_prescriptions = list(Patient_history.objects.values().filter(user_id = patient_id))
    return render(request,'patient_prescriptions.html',{'prescriptions':patient_prescriptions})

    
def load_doctors(request):
    if request.is_ajax():
        problem = request.GET.get('problem')
        doctor_id = User_type.objects.values('user_id').filter(specialization=problem)
        doctors = User.objects.values('first_name', 'last_name').filter(id__in=doctor_id)
        list = []
        for doctor in doctors:
            
            list.append(doctor['first_name']+" "+doctor['last_name'])
            
        data = {
                'list': list,
            }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request,'reception.html',{})
   
def send_prescriptions(request,patient_id):
    diagnosis = request.POST['diagnosis']
    blood_pressure = request.POST['bp']
    weight =request.POST['weight']
    sugar = request.POST['sugar']
    list_of_medicines = request.POST.getlist('medicine')
    morning_intake = request.POST.getlist('checkbox1[]')
    afternoon_intake = request.POST.getlist('checkbox2[]')
    evening_intake = request.POST.getlist('checkbox3[]')
    tests = request.POST['tests']
    x = 1
    for medicine in list_of_medicines:
        Patient_history.objects.create(date = date.today(), diagnosis = diagnosis, blood_pressure=blood_pressure, weight=weight,
                                sugar=sugar,medicine = medicine,morning_intake = True if str(x) in morning_intake else False,
                                afternoon_intake = True if str(x) in afternoon_intake else False, evening_intake = True if str(x) in evening_intake else False,
                                days = 1, tests = tests,user_id=patient_id)
        x = x+1
    patient = Patient.objects.get(id = patient_id)
    patient.is_seen = True
    patient.save()
    return redirect('doctors')