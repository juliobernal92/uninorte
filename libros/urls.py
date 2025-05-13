# libros/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LibroViewSet, CalificacionViewSet

router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
