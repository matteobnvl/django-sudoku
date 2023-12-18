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
    sudoku = [
        [2,0,0,6,3,9,8,0,1],
        [3,1,0,2,8,0,7,0,0],
        [0,0,5,0,0,0,2,3,9],
        [7,3,0,0,5,0,0,0,0],
        [0,0,8,1,6,7,0,2,5],
        [5,0,0,0,4,0,0,8,7],
        [6,9,0,0,0,8,0,1,0],
        [0,0,0,5,9,0,6,0,2],
        [1,0,0,3,2,6,0,0,8]
    ]
    solution = [
        [2,7,4,6,3,9,8,5,1],
        [3,1,9,2,8,5,7,4,6],
        [8,6,5,7,1,4,2,3,9],
        [7,3,1,8,5,2,9,6,4],
        [9,4,8,1,6,7,3,2,5],
        [5,2,6,9,4,3,1,8,7],
        [6,9,2,4,7,8,5,1,3],
        [4,8,3,5,9,1,6,7,2],
        [1,5,7,3,2,6,4,9,8]
    ]
    return render(request, 'dashboard/index.html')


def profil(request):
    return render(request, 'profile/index.html')


def page_not_found_view(request):
    return render(request,'error.html', context={})