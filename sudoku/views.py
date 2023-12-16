from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

# Create your views here.


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {e}")
            return redirect('dashboard')
    else: 
        form = RegisterForm()
    return render(request, 'registration/register.html',  {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')