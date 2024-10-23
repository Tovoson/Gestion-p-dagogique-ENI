from django.db import models

class Materiel(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('utilise', 'Utilisé'),
        ('rendu', 'Rendu'),
    ]

    id_materiel = models.AutoField(primary_key=True)
    nom_materiel = models.CharField(max_length=100)
    nombre = models.CharField(max_length=10)
    id_admin = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponible')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_materiel
    
class Admin (models.Model):
    id_admin = models.CharField(primary_key=True, max_length=10)
    nom_admin = models.CharField(max_length=100)
    # photo_admin = models.ImageField()
    fonction = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.id_admin
    
class Utilisation (models.Model):
    id_utils = models.AutoField(primary_key=True)
    id_admin = models.CharField(max_length=100)
    id_materiel = models.CharField(max_length=100)
    id_etudiant = models.CharField(max_length=100)

    def __str__(self):
        return self.id_utils
