from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import login
from django.urls import reverse
from .forms import RegisterForm, SudokuForm, ProfilForm
from .models import Sudoku, Player
from .sudoku import SudokuEntity
import json

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                print(f"Erreur lors de la sauvegarde : {e}")
        else:
            errors = form.errors
    else: 
        form = RegisterForm()
    return render(request, 'registration/register.html',  {'form': form, 'errors': errors})

@login_required
def dashboard(request):
    all_sudoku = Sudoku.objects.filter(player=request.user)
    sudokus = Sudoku.objects.filter(player=request.user, is_finish=False)
    return render(request, 'dashboard/index.html', {'sudokus': sudokus, 'nb_sudoku': len(all_sudoku)})

@login_required
def generate_sudoku(request):
    sudoku = SudokuEntity(niveau=request.user.niveau)
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
        'tableau': json.loads(sudoku.tableau),
        'sudoku': sudoku,
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
        
@csrf_exempt
@login_required
def verif_sudoku(request):
    if request.method == 'POST':
        id_sudoku = request.POST.get('id')
        
        sudoku = Sudoku.objects.get(id=id_sudoku)
        tableau = json.loads(sudoku.tableau)
        solution = json.loads(sudoku.solution)
        errors = []
        for indice_lignes in range(len(tableau)):
            for indice_case in range(len(tableau[indice_lignes])):
                if tableau[indice_lignes][indice_case] >= 10:
                    if tableau[indice_lignes][indice_case]/10 != solution[indice_lignes][indice_case]:
                        error = {
                            'key': f"{str(indice_lignes)}-{str(indice_case)}",
                            'value': False
                        }
                        errors.append(error)
        if errors == []:
            sudoku.is_finish = True
            sudoku.save()
            return JsonResponse({'success': True, 'message': 'Bravo vous avez réussis le sudoku'})
        return JsonResponse({'success': True, 'message': "Vous n'avez pas réussis, il y a des erreurs", 'data': errors})
    
@csrf_exempt
@login_required
def check_error(request):
    if request.method == 'POST':
        id_sudoku = request.POST.get('id')
        
        sudoku = Sudoku.objects.get(id=id_sudoku)
        tableau = json.loads(sudoku.tableau)
        solution = json.loads(sudoku.solution)
        tableau_verif = []
        for indice_lignes in range(len(tableau)):
            for indice_case in range(len(tableau[indice_lignes])):
                if tableau[indice_lignes][indice_case] >= 10:
                    value = {
                        'key': f"{str(indice_lignes)}-{str(indice_case)}",
                        'value': (tableau[indice_lignes][indice_case]/10) == solution[indice_lignes][indice_case]
                    }
                    tableau_verif.append(value)
        return JsonResponse({'success': True, 'data': tableau_verif})


def profil(request):
    nb_sudoku = len(Sudoku.objects.filter(player=request.user.id))
    nb_sudoku_finished = len(Sudoku.objects.filter(player=request.user.id, is_finish=True))
    stats = {
        'nb_sudoku': nb_sudoku,
        'nb_sudoku_finished': nb_sudoku_finished
    }
    if request.method == 'POST':
        player = Player.objects.get(id=request.user.id)
        if len(Player.objects.filter(~Q(id=request.user.id), email=request.POST.get('email'))) < 1:
            player.email = escape(request.POST.get('email'))
            player.pseudo = escape(request.POST.get('pseudo'))
            if request.POST.get('niveau') in ['easy', 'medium', 'hard']:
                player.niveau = escape(request.POST.get('niveau'))
            player.save()
        else:
            return render(request, 'profile/index.html', {'errors': "L'email renseigné est déjà utilisé", 'stats': stats})
    return render(request, 'profile/index.html', {'stats': stats})

def render_404(request, exception):
    return render(request, '404.html', status=404)