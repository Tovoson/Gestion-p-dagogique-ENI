from rest_framework import serializers
from .models import *

class MaterielSerializers(serializers.ModelSerializer):
    class Meta :
        model = Materiel
        fields = '__all__'

class AdminSerializers(serializers.ModelSerializer):
    class Meta :
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'mot_de_passe': {'write_only': True}  # Pour ne pas renvoyer le mot de passe dans les réponses
        }

class UtilisationSerializers(serializers.ModelSerializer):
    class Meta :
        model = Utilisation
        fields = '__all__'
