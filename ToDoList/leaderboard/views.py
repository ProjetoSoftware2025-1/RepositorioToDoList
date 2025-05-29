from django.shortcuts import render
from django.views.generic import ListView
from tasks.models import Task

# Create your views here.
class Homepage(ListView):
    template_name = "dashboard.html"
    model = Task
