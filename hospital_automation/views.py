from django.shortcuts import render, redirect
from .models import patient
from django.conf.urls import *

def doctors():
    pass

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
 




