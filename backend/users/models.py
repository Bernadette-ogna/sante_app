from django.db import models

# Create your models here.
# Freelance Fullstack Starter

## backend/users/models.
from django.db import models

class Person(models.Model):
    STATUS_CHOICES=[('travailleur','Travailleur'),('non_travailleur','Non Travailleur')]
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=30)
    ville=models.CharField(max_length=100)
    statut=models.CharField(max_length=30,choices=STATUS_CHOICES)
    profession=models.CharField(max_length=100,blank=True)
    entreprise=models.CharField(max_length=100,blank=True)
    salaire=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    niveau_etude=models.CharField(max_length=100,blank=True)
    recherche_emploi=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

