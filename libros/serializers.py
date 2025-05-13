# libros/serializers.py
from rest_framework import serializers
from .models import Autor, Libro, Calificacion
from django.contrib.auth.models import User

# Serializador para Autor
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

# Serializador para Libro
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

# Serializador para Calificación
class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'
