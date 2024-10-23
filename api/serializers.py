from rest_framework import serializers
from .models import *

class MaterielSerializers(serializers.ModelSerializer):
    class Meta :
        model = Materiel
        fields = ('id_materiel','nom_materiel', 'nombre', 'id_admin', 'status')

class AdminSerializers(serializers.ModelSerializer):
    class Meta :
        model = Admin
        fields = ('id_admin', 'nom_admin', 'fonction', 'mot_de_passe')

class UtilisationSerializers(serializers.ModelSerializer):
    class Meta :
        model = Utilisation
        fields = ('id_admin', 'nom_admin', 'fonction', 'mot_de_passe')
