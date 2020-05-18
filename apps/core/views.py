from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def landingPage(request):

    return render(request, 'core/index.html',{})
