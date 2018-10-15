from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
from datetime import datetime
from hospital_automation.serializers import PatientSerializer

def doctors(request):
    return render(request,'incoming_patient.html', {} )


def receive_patient(request):
    if request.method == 'GET':
        incoming_patient = list(Patient.objects.values().filter(is_seen = False))
        serializer = PatientSerializer(incoming_patient, many = True, context = {'request':request})
        return JsonResponse(serializer.data, safe = False)


def reception(request):
    return render(request,'reception.html',{})
