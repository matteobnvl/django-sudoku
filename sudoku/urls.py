from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profil/', views.profil, name="profil"),
    path('generate/', views.generate_sudoku, name="generate"),
    path('play/<int:pk>', views.play, name="play"),
    path('insert/', views.insert, name="insert"),
    path('delete/', views.delete, name="delete"),
    path('finish/', views.verif_sudoku, name="valid_sudoku"),
    path('check/', views.check_error, name="check")
]
