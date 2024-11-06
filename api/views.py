from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout



class MaterielViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Materiel.objects.all()
    serializer_class = MaterielSerializers

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)
        

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
           
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def retrieve(self, request, pk=None):
        material = self.queryset.get(pk=pk)
        serializer = self.serializer_class(material)
        return Response(serializer.data)

    def update(self, request, pk=None):
        material = self.queryset.get(pk=pk)
        serializer = self.serializer_class(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        material = self.queryset.get(pk=pk)
        try:
            material.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except material.DoesNotExist:
            # Retourne une erreur 404 si l'objet n'existe pas
            return Response({f"error": "L'objet Material qui a l'id  n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
    
    # Admin
class AdminViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializers

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        admin = self.queryset.get(pk=pk)
        serializer = self.serializer_class(admin)
        return Response(serializer.data)

    def update(self, request, pk=None):
        admin = self.queryset.get(pk=pk)
        serializer = self.serializer_class(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        admin = self.queryset.get(pk=pk)
        admin.delete()
        return Response(status=204)

    @action(detail=False, methods=['post'], url_path='auth_admin')
    def auth_admin(self, request):
        id_admin = request.data.get('id_admin')
        mot_de_passe = request.data.get('mot_de_passe')
        user = authenticate(request, id_admin=id_admin, mot_de_passe=mot_de_passe)
        try:
            admin = Admin.objects.get(id_admin=id_admin)
            if admin.mot_de_passe == mot_de_passe:  # Note: Il faudrait utiliser un hash en production
                serializer = self.serializer_class(admin)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            pass
        
        return Response(
            {'error': 'Identifiants invalides'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    
        # Utilisation
class UtilisationViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Utilisation.objects.all()
    serializer_class = UtilisationSerializers

    def list(self, request):
        # Récupérer les utilisations avec estRendu = True
        rendus = Utilisation.objects.filter(estRendu=True)
        # Récupérer les utilisations avec estRendu = False
        non_rendus = Utilisation.objects.filter(estRendu=False)

        # Sérialiser les deux ensembles de données
        rendus_serializer = self.serializer_class(rendus, many=True)
        non_rendus_serializer = self.serializer_class(non_rendus, many=True)

        # Retourner les données dans un format structuré
        return Response({
            "rendus": rendus_serializer.data,
            "non_rendus": non_rendus_serializer.data,
        })

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        utilisation = self.queryset.get(pk=pk)
        serializer = self.serializer_class(utilisation)
        return Response(serializer.data)

    def update(self, request, pk=None):
        utilisation = self.queryset.get(pk=pk)
        serializer = self.serializer_class(utilisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        utilisation = self.queryset.get(pk=pk)
        utilisation.delete()
        return Response(status=204)
    
    @action(detail=False, methods=['get'], url_path='materiels-plus-utilises')
    def materiels_plus_utilises(self, request):
        stats = Utilisation.objects.values(
            'id_materiel',
            'id_materiel__nom_materiel',
        ).annotate(
            nombre_utilisations=Count('id_materiel')
        ).order_by('-nombre_utilisations').first()  # On utilise .first() au lieu de [:limit]

        # Si aucun résultat n'est trouvé
        if not stats:
            return Response({
                'message': 'Aucune utilisation trouvée'
            })

        # Formater la réponse pour un seul élément
        formatted_stat = {
            'id': stats['id_materiel'],
            'nom': stats['id_materiel__nom_materiel'],
            'utilisations': stats['nombre_utilisations']
        }

        return Response(formatted_stat)

    @action(detail=False, methods=['get'], url_path='utilisateur-plus-frequent')
    def utilisateur_plus_frequent(self, request):
        stats = Utilisation.objects.values(
            'matricule',
            'nom',
            'telephone'
        ).annotate(
            nombre_utilisations=Count('id_utils')
        ).order_by('-nombre_utilisations').first()

        if not stats:
            return Response({
                'message': 'Aucune utilisation trouvée'
            })

        formatted_stat = {
            'nom': stats['nom'],
            'matricule': stats['matricule'],
            'telephone': stats['telephone'],
            'utilisations': stats['nombre_utilisations']
        }

        return Response(formatted_stat)

    @action(detail=False, methods=['get'], url_path='admin-plus-actif')
    def admin_plus_actif(self, request):
        stats = Utilisation.objects.values(
            'id_admin',
            'id_admin__nom_admin',  # Correction ici : nom_admin au lieu de nom
        ).annotate(
            nombre_gestions=Count('id_utils')
        ).order_by('-nombre_gestions').first()

        if not stats:
            return Response({
                'message': 'Aucun admin trouvé'
            })

        formatted_stat = {
            'id': stats['id_admin'],
            'nom': stats['id_admin__nom_admin'],  # Mettons 'nom' dans la réponse pour garder une API cohérente
            'nombre_gestions': stats['nombre_gestions']
        }

        return Response(formatted_stat)

    @action(detail=False, methods=['get'], url_path='statistiques-materiels')
    def statistiques_materiels(self, request):
        stats = Utilisation.objects.values(
            'id_materiel',
            'id_materiel__nom_materiel'
        ).annotate(
            nombre_utilisations=Count('id_materiel')
        ).order_by('-nombre_utilisations')

        # Préparer les données dans le format requis pour Chart.js
        data = {
            'labels': [item['id_materiel__nom_materiel'] for item in stats],
            'datasets': [{
                'label': 'Utilisation des matériels',
                'data': [item['nombre_utilisations'] for item in stats],
                'backgroundColor': [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                ],
                'borderColor': [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                    '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                ],
            }]
        }

        return Response(data)


    @action(detail=False, methods=['get'], url_path='utilisation-30-jours')
    def utilisation_30_jours(self, request):
        # Calculer la date d'il y a 30 jours
        date_30_jours = datetime.now() - timedelta(days=30)
        
        # Récupérer les utilisations par jour
        stats = Utilisation.objects.filter(
            date_debut__gte=date_30_jours
        ).annotate(
            date=TruncDate('date_debut')
        ).values('date').annotate(
            nombre=Count('id_utils')
        ).order_by('date')

        # Créer un dictionnaire avec tous les jours (même ceux sans utilisation)
        all_dates = {}
        current_date = date_30_jours.date()
        end_date = datetime.now().date()
        
        while current_date <= end_date:
            all_dates[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)

        # Remplir avec les données réelles
        for stat in stats:
            date_str = stat['date'].strftime('%Y-%m-%d')
            all_dates[date_str] = stat['nombre']

        # Préparer les données pour Chart.js
        data = {
            'labels': list(all_dates.keys()),
            'datasets': [{
                'label': 'Nombre d\'utilisations par jour',
                'data': list(all_dates.values()),
                'fill': False,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1
            }]
        }

        return Response(data)

    @action(detail=False, methods=['get'], url_path='utilisations-quotidiennes')
    def utilisations_quotidiennes(self, request):
        # Obtenir les 7 derniers jours
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)

        stats = (
            Utilisation.objects
            .filter(date_debut__range=[start_date, end_date])
            .annotate(date=TruncDate('date_debut'))
            .values('date', 'nom')
            .annotate(nombre_utilisations=Count('id_utils'))
            .order_by('date', 'nom')
        )

        # Organiser les données pour Chart.js
        dates = list(set(item['date'].strftime('%Y-%m-%d') for item in stats))
        utilisateurs = list(set(item['nom'] for item in stats))
        
        # Créer un dictionnaire pour faciliter l'accès aux données
        data_dict = {(item['date'].strftime('%Y-%m-%d'), item['nom']): item['nombre_utilisations'] for item in stats}
        
        # Préparer les datasets pour chaque utilisateur
        datasets = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
        
        for i, utilisateur in enumerate(utilisateurs):
            color = colors[i % len(colors)]
            data = [data_dict.get((date, utilisateur), 0) for date in dates]
            datasets.append({
                'label': utilisateur,
                'data': data,
                'backgroundColor': color,
                'borderColor': color,
                'fill': False
            })

        chart_data = {
            'labels': dates,
            'datasets': datasets
        }

        return Response(chart_data)

    @action(detail=False, methods=['get'], url_path='utilisations-par-jour')
    def utilisations_par_jour(self, request):
        # Récupérer les 7 derniers jours par défaut
        jours = int(request.query_params.get('jours', 7))
        
        # Calculer la date de début
        date_debut = datetime.now().date() - timedelta(days=jours-1)
        
        # Récupérer les statistiques
        stats = Utilisation.objects.filter(
            date_debut__date__gte=date_debut
        ).annotate(
            jour=TruncDate('date_debut')
        ).values(
            'jour',
            'id_materiel__nom_materiel'
        ).annotate(
            nombre=Count('id_utils')
        ).order_by('jour', 'id_materiel__nom_materiel')

        # Organiser les données pour le graphique
        materiels = list(set(item['id_materiel__nom_materiel'] for item in stats))
        jours = list(set(item['jour'].strftime('%Y-%m-%d') for item in stats))
        jours.sort()

        # Préparer les datasets
        datasets = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', 
                '#FF9F40', '#00FF00', '#FF00FF', '#800080', '#008080']
                
        for i, materiel in enumerate(materiels):
            data = []
            for jour in jours:
                nombre = next(
                    (item['nombre'] for item in stats 
                    if item['id_materiel__nom_materiel'] == materiel 
                    and item['jour'].strftime('%Y-%m-%d') == jour),
                    0
                )
                data.append(nombre)
                
            datasets.append({
                'label': materiel,
                'data': data,
                'backgroundColor': colors[i % len(colors)],
                'borderColor': colors[i % len(colors)],
                'tension': 0.1
            })

        chart_data = {
            'labels': jours,
            'datasets': datasets
        }

        return Response(chart_data)
