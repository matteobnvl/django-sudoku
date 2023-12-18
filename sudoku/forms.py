from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player, Sudoku

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = Player
        fields = ['pseudo', 'email', 'password1', 'password2']
        
class SudokuForm(forms.ModelForm):
    class Meta:
        model = Sudoku
        fields = ['tableau', 'solution', 'niveau']