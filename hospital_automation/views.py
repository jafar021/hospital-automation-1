from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines
from datetime import datetime, date
from hospital_automation.serializers import PatientSerializer
from django.shortcuts import render, redirect
from django.conf.urls import *
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

counter = 1
counter_for_dispensary = 1


@login_required
def doctors(request):
    user_group = request.user.groups.values_list('name', flat=True)[0]
    if user_group == 'Doctor':
        patient = list(Patient.objects.values().filter(is_seen=False, assigned_doctor=(
            request.user.first_name+" "+request.user.last_name)))
        print(request.user.username)
        return render(request, 'incoming_patient.html', {'incoming_patient': patient})
    else:
        return render(request, 'index.html', {'user_group': 'Doctor'})


def receive_patient(request):
    global counter
    if request.method == 'GET' and counter == 0:
        incoming_patient = list(Patient.objects.values().filter(is_seen=False, assigned_doctor=(request.user.first_name+" "+request.user.last_name)).order_by('-id')[:1])
        serializer=PatientSerializer(
            incoming_patient, many=True, context={'request': request})
        counter=1
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({}, safe=False)


@login_required
def reception(request):
    user_group=request.user.groups.values_list('name', flat=True)[0]
    if(user_group == 'Receptionist'):
        global counter
        if request.method == 'GET':
            return render(request, 'reception.html', {})
        elif request.method == 'POST':
            first_name=request.POST['First Name']
            last_name=request.POST['Last Name']
            father_name=request.POST['Father name']
            address=request.POST['Address']
            city=request.POST['City']
            state=request.POST['State']
            zip_code=request.POST['Postal/ZIP code']
            country=request.POST['Country']
            country_code=request.POST['country code']
            contact_number=request.POST['Contact Number']
            date=request.POST['todays date']
            problem=request.POST['problem']
            alloted_doctor=request.POST['Doctor name']
            Patient.objects.create(first_name=first_name, last_name=last_name, guardian_name=father_name, address=address,
                                   city=city, state=state, zip_code=zip_code, country=country,
                                   country_code=country_code, phone_number=contact_number, date=date, problem_name=problem, assigned_doctor=alloted_doctor)
            counter=0
            return redirect('reception')
    else:
        return render(request, 'index.html', {'user_group': 'Receptionist'})



@csrf_exempt
def autocomplete(request, id):
    if request.is_ajax():
        queryset=User_type.objects.filter(
            specialization__startswith=request.GET['search'])
        list=[]
        for problem in queryset:
            if problem.specialization not in list:
                list.append(problem.specialization)
        data={
            'list': list,
        }
        print(list)
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request, 'reception.html', {})


def prescriptions(request, patient_id):
    patient_prescriptions=Patient.objects.values().filter(id=patient_id)
    print(patient_prescriptions)
    return render(request, 'patient_prescriptions.html', {'prescriptions': patient_prescriptions})

def load_doctors(request):
    if request.is_ajax():
        problem=request.GET.get('problem')
        doctor_id=User_type.objects.values(
            'user_id').filter(specialization=problem)
        doctors=User.objects.values(
            'first_name', 'last_name').filter(id__in=doctor_id)
        list=[]
        for doctor in doctors:

            list.append(doctor['first_name'] + " " + doctor['last_name'])

        data={
            'list': list,
        }
        return JsonResponse(data)
    if request.method == 'GET':
        return render(request,'reception.html',{})
   
def send_prescriptions(request,patient_id):
    global counter_for_dispensary
    diagnosis = request.POST['diagnosis']
    blood_pressure = request.POST['bp']
    weight =request.POST['weight']
    sugar = request.POST['sugar']
    list_of_medicines = request.POST.getlist('medicine')
    morning_intake = request.POST.getlist('checkbox1[]')
    afternoon_intake = request.POST.getlist('checkbox2[]')
    evening_intake = request.POST.getlist('checkbox3[]')
    tests = request.POST['tests']
    medicine_intake = 1
    for medicine in list_of_medicines:
        Patient_history.objects.create(date=date.today(), diagnosis=diagnosis, blood_pressure=blood_pressure, weight=weight,
                                sugar=sugar, medicine=medicine, morning_intake=True if str(
                                    medicine_intake) in morning_intake else False,
                                afternoon_intake=True if str(medicine_intake) in afternoon_intake else False, evening_intake=True if str(medicine_intake) in evening_intake else False,
                                days=1, tests=tests, user_id=patient_id)
        medicine_intake=medicine_intake+1
    patient=Patient.objects.get(id=patient_id)
    patient.is_seen=True
    patient.save()
    counter_for_dispensary = 0
    return redirect('doctors')

def doctor_details(request):

    doctor_id=User_type.objects.values('user_id').filter(flag=1)
    doctor_specializations=User_type.objects.values(
        'specialization').filter(flag=1)
    doctors_name=User.objects.values(
        'first_name', 'last_name').filter(id__in=doctor_id)
    doctors_list=[]

    for name in range(0, len(doctors_name)):
        doctors_display_details={}
        doctors_display_details['first_name']=doctors_name[name]['first_name']
        doctors_display_details['last_name']=doctors_name[name]['last_name']
        doctors_display_details['specialization']=doctor_specializations[name]['specialization']
        doctors_list.append(doctors_display_details)
    return render(request, 'doctor_details.html', {'doctors_list': doctors_list})


def helpers(request):
    helper_details=Helpers_nurses.objects.values()
    return render(request, 'helpers.html', {'helper_details': helper_details})


def index(request):
    return render(request, 'index.html', {})

@login_required
def patient_to_dispensary(request):
    user_group = request.user.groups.values_list('name', flat=True)[0]
    if user_group == 'Dispensary':
        patient_ids = Patient_history.objects.values('user_id').distinct().filter(is_done=False)
        patient_names = list(Patient.objects.values('id','first_name','last_name').filter(id__in=patient_ids))
        return render(request, 'dispensary.html', {'incoming_patient': patient_names})
    else:
        return render(request, 'index.html', {'user_group': 'Dispensary'})

@login_required
def receive_incoming_patient_to_dispensary(request):
    global counter_for_dispensary
    if request.method == 'GET' and counter_for_dispensary == 0:
        patient_ids = Patient_history.objects.values('user_id').distinct().filter(is_done=False)
        patient_names = list(Patient.objects.values('id','first_name', 'last_name','guardian_name','problem_name','assigned_doctor').filter(id__in=patient_ids).order_by('-id')[:1])
        serializer = PatientSerializer(patient_names, many=True, context={'request': request})
        counter_for_dispensary = 1
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({}, safe=False)

@login_required
def medication_of_patient(request,patient_id):
    medication = Patient_history.objects.values('medicine','morning_intake','afternoon_intake','evening_intake').filter(user_id = patient_id)
    pass
