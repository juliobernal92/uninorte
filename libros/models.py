from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    genero = models.CharField(max_length=100)
    url_libro = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puntaje = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.libro.nombre}: {self.puntaje}"
