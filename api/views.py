from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response


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
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

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
        material.delete()
        return Response(status=204)
    
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
    
        # Utilisation
class UtilisationViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Utilisation.objects.all()
    serializer_class = UtilisationSerializers

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