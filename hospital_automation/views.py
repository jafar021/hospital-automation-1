from django.shortcuts import render

def doctors():
    pass

def reception(request): 
    return render(request, 'reception.html', {})

