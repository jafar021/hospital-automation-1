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

def doctors(request):
    return render(request,'incoming_patient.html', {} )


def receive_patient(request):
    if request.method == 'GET':
        incoming_patient = list(Patient.objects.values().filter(is_seen = False))
        serializer = PatientSerializer(incoming_patient, many = True, context = {'request':request})
        return JsonResponse(serializer.data, safe = False)


def reception(request):
    return render(request,'reception.html',{})
def reception(request):
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
        patient.objects.create(first_name=first_name, last_name=last_name, guardian_name=father_name, address=address, 
                                 city=city, state=state, zip_code=zip_code, country=country, 
                                country_code=country_code, phone_number=contact_number, date=date, problem_name=problem, assigned_doctor=alloted_doctor)
        
        return redirect('reception')       

@csrf_exempt
def autocomplete(request, id):
    if request.is_ajax():
        queryset = user_type.objects.filter(specialization__startswith=request.GET['search'])
        list = []        
        for i in queryset:
            if i.specialization not in list:
                list.append(i.specialization)
        data = {
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request,'reception.html',{})




