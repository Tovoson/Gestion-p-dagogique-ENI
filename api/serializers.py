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

class UtilisationSerializers(serializers.ModelSerializer):
    class Meta :
        model = Utilisation
        fields = '__all__'
