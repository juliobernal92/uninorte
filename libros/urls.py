# libros/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    # AUTOR
    path('autores/', views.listar_autores, name='listar_autores'),
    path('autores/crear/', views.crear_autor, name='crear_autor'),
    path('autores/<int:pk>/', views.obtener_autor, name='obtener_autor'),
    path('autores/<int:pk>/actualizar/', views.actualizar_autor, name='actualizar_autor'),
    path('autores/<int:pk>/eliminar/', views.eliminar_autor, name='eliminar_autor'),

    # LIBRO
    path('libros/', views.listar_libros, name='listar_libros'),
    path('libros/crear/', views.crear_libro, name='crear_libro'),
    path('libros/<int:pk>/', views.obtener_libro, name='obtener_libro'),
    path('libros/<int:pk>/actualizar/', views.actualizar_libro, name='actualizar_libro'),
    path('libros/<int:pk>/eliminar/', views.eliminar_libro, name='eliminar_libro'),

    # GENERO
    path('generos/', views.listar_generos, name='listar_generos'),
    path('generos/crear/', views.crear_genero, name='crear_genero'),
    path('generos/<int:pk>/', views.obtener_genero, name='obtener_genero'),
    path('generos/<int:pk>/actualizar/', views.actualizar_genero, name='actualizar_genero'),
    path('generos/<int:pk>/eliminar/', views.eliminar_genero, name='eliminar_genero'),

    # CALIFICACION
    path('calificaciones/', views.listar_calificaciones, name='listar_calificaciones'),
    path('calificaciones/crear/', views.crear_calificacion, name='crear_calificacion'),
    path('calificaciones/<int:pk>/', views.obtener_calificacion, name='obtener_calificacion'),
    path('calificaciones/<int:pk>/actualizar/', views.actualizar_calificacion, name='actualizar_calificacion'),
    path('calificaciones/<int:pk>/eliminar/', views.eliminar_calificacion, name='eliminar_calificacion'),
]