from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from django.http import Http404
from django.urls import reverse
from .forms import RegisterForm, SudokuForm
from .models import Sudoku
from .sudoku import SudokuEntity
import json

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
    sudokus = Sudoku.objects.filter(player=request.user)
    return render(request, 'dashboard/index.html', {'sudokus': sudokus})

@login_required
def generate_sudoku(request):

    sudoku = SudokuEntity()
    sudoku.generate()
    form = SudokuForm({
        'tableau': sudoku.tableau,
        'solution': sudoku.solution,
        'niveau': sudoku.niveau
    })
    form.instance.player = request.user
    sudoku_instance = form.save()
    id_sudoku = sudoku_instance.id
    return redirect('play', pk=id_sudoku)

@login_required
def play(request, pk):
    player = request.user
    sudoku = get_object_or_404(Sudoku, id=pk, player=player)
    return render(request, 'play/index.html', {
        'sudoku': json.loads(sudoku.tableau),
        'id_sudoku': sudoku.id
    })
    
@csrf_exempt   
@login_required
def insert(request):
    if request.method == 'POST':
        array_case_key = request.POST.get('arrayCase[key]', None)
        array_case_value = request.POST.get('arrayCase[value]', None)
        id_sudoku = request.POST.get('id', None)
        sudoku = Sudoku.objects.get(id=id_sudoku)
        tableau = json.loads(sudoku.tableau)
        tableau[int(array_case_key[0])][int(array_case_key[-1])] = int(array_case_value) * 10
        sudoku.tableau = json.dumps(tableau, separators=(',', ':'))
        sudoku.save()
    return JsonResponse({'success': True, 'message': 'Données reçues avec succès'})


@csrf_exempt   
@login_required
def delete(request):
    if request.method == 'POST':
        array_case_key = request.POST.get('attrCase', None)
        id_sudoku = request.POST.get('id', None)
        sudoku = Sudoku.objects.get(id=id_sudoku)
        tableau = json.loads(sudoku.tableau)
        if tableau[int(array_case_key[0])][int(array_case_key[-1])] == 0 or tableau[int(array_case_key[0])][int(array_case_key[-1])] >= 10:
            tableau[int(array_case_key[0])][int(array_case_key[-1])] = 0
            sudoku.tableau = json.dumps(tableau, separators=(',', ':'))
            sudoku.save()
            return JsonResponse({'success': True, 'message': 'Données reçues avec succès'})
        else: 
            return JsonResponse({'success': False, 'message': 'Impoosible de supprimer ces données'})


def profil(request):
    return render(request, 'profile/index.html')


def page_not_found_view(request):
    return render(request,'error.html', context={})