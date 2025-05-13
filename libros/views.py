from django.shortcuts import render
from rest_framework import viewsets
from .models import Autor, Libro, Calificacion
from rest_framework.permissions import IsAuthenticated
from .serializers import AutorSerializer, LibroSerializer, CalificacionSerializer

# ViewSet para Autor
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Libro
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Calificación
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated] 
