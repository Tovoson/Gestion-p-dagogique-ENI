from django.db import models

class Materiel(models.Model):

    id_materiel = models.AutoField(primary_key=True)
    nom_materiel = models.CharField(max_length=100, default='')
    nombre = models.CharField(max_length=10, default='0')
    id_admin = models.ForeignKey('Admin', on_delete=models.CASCADE, to_field='id_admin')
    status = models.CharField(max_length=10, default='disponible')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_materiel)
    
class Admin (models.Model):
    id_admin = models.CharField(primary_key=True, max_length=10)
    nom_admin = models.CharField(max_length=100, default='')
    photo_admin = models.ImageField(default='fallback.png', blank=True)
    mot_de_passe = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.id_admin)
    
class Utilisation (models.Model):
    id_utils = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey('Admin', on_delete=models.CASCADE, to_field='id_admin')
    id_materiel = models.ForeignKey('Materiel', on_delete=models.CASCADE, to_field='id_materiel')
    matricule = models.CharField(max_length=100, default='')
    nom = models.CharField(max_length=100, default='')
    telephone = models.CharField(max_length=100, default='')
    niveau = models.CharField(max_length=100, default='')
    date_debut = models.DateTimeField(null=True)
    date_fin_prevu = models.DateTimeField(null=True)
    nombre = models.CharField(max_length=10, default='0')
    estRendu = models.BooleanField(default=False)
    dateRendu = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.id_utils)
