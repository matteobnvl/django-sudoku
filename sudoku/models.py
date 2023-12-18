from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email doit être renseigné')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)


class Player(AbstractBaseUser, PermissionsMixin):
    TABLEAU_MAX_LENGTH = 250
    pseudo = models.CharField(max_length=TABLEAU_MAX_LENGTH)
    email = models.EmailField(max_length=TABLEAU_MAX_LENGTH, unique=True)
    password = models.CharField(max_length=TABLEAU_MAX_LENGTH)
    created_at = models.DateTimeField('user created', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['pseudo']
    
    objects = UserManager()
    
    def __str__(self):
        return self.pseudo

class Sudoku(models.Model):
    TABLEAU_MAX_LENGTH = 250
    NIVEAU_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    tableau = models.CharField(max_length=TABLEAU_MAX_LENGTH)
    solution = models.CharField(max_length=TABLEAU_MAX_LENGTH)
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOICES)
    created_at = models.DateTimeField('sudoku created', auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Sudoku {self.id} - {self.niveau} - {self.created_at}"
