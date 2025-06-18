from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Autor, Libro, Genero, Calificacion
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionSerializer

########################################################################################################
# ---------- AUTOR ----------
########################################################################################################
# listar_autores, crear_autor, etc.

# Listar autores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_autores(request):
    autores = Autor.objects.all()
    serializer = AutorSerializer(autores, many=True)
    return Response(serializer.data)

# Crear autor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_autor(request):
    serializer = AutorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener autor por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_autor(request, pk):
    try:
        autor = Autor.objects.get(pk=pk)
    except Autor.DoesNotExist:
        return Response({'error': 'Autor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AutorSerializer(autor)
    return Response(serializer.data)

# Actualizar autor
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_autor(request, pk):
    try:
        autor = Autor.objects.get(pk=pk)
    except Autor.DoesNotExist:
        return Response({'error': 'Autor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AutorSerializer(autor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Eliminar autor
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_autor(request, pk):
    try:
        autor = Autor.objects.get(pk=pk)
    except Autor.DoesNotExist:
        return Response({'error': 'Autor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    autor.delete()
    return Response({'mensaje': 'Autor eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


########################################################################################################
# ---------- LIBRO ----------
########################################################################################################
# listar_libros, crear_libro, etc.

# Listar libros
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_libros(request):
    libros = Libro.objects.all()
    serializer = LibroSerializer(libros, many=True)
    return Response(serializer.data)

# Crear Libro
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_libro(request):
    serializer = LibroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener libro por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({'error': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LibroSerializer(libro)
    return Response(serializer.data)

# Actualizar Libro
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({'error': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LibroSerializer(libro, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Eliminar libro
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({'error': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    libro.delete()
    return Response({'mensaje': 'Libro eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

########################################################################################################
# ---------- GENERO ----------
########################################################################################################
# listar_generos, crear_genero, etc.

# Listar generos
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_generos(request):
    generos = Genero.objects.all()
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data)

# Crear Genero
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_genero(request):
    serializer = GeneroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener genero por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_genero(request, pk):
    try:
        genero = Genero.objects.get(pk=pk)
    except Genero.DoesNotExist:
        return Response({'error': 'Genero no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GeneroSerializer(genero)
    return Response(serializer.data)

# Actualizar genero
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_genero(request, pk):
    try:
        genero = Genero.objects.get(pk=pk)
    except Genero.DoesNotExist:
        return Response({'error': 'Genero no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GeneroSerializer(genero, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Eliminar genero
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_genero(request, pk):
    try:
        genero = Genero.objects.get(pk=pk)
    except Genero.DoesNotExist:
        return Response({'error': 'Genero no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    genero.delete()
    return Response({'mensaje': 'Genero eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

########################################################################################################
# ---------- CALIFICACION ----------
########################################################################################################
# listar_calificaciones, crear_calificacion, etc.

# Listar calificaciones del usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_calificaciones(request):
    calificaciones = Calificacion.objects.filter(user=request.user)
    serializer = CalificacionSerializer(calificaciones, many=True)
    return Response(serializer.data)

# Crear una calificación (se asocia automáticamente al usuario autenticado)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_calificacion(request):
    serializer = CalificacionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()  # El serializer ya toma request.user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener una calificación por ID (solo si pertenece al usuario)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_calificacion(request, pk):
    try:
        calificacion = Calificacion.objects.get(pk=pk, user=request.user)
    except Calificacion.DoesNotExist:
        return Response({'error': 'Calificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CalificacionSerializer(calificacion)
    return Response(serializer.data)

# Actualizar una calificación (solo si pertenece al usuario)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_calificacion(request, pk):
    try:
        calificacion = Calificacion.objects.get(pk=pk, user=request.user)
    except Calificacion.DoesNotExist:
        return Response({'error': 'Calificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CalificacionSerializer(calificacion, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Eliminar una calificación (solo si pertenece al usuario)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_calificacion(request, pk):
    try:
        calificacion = Calificacion.objects.get(pk=pk, user=request.user)
    except Calificacion.DoesNotExist:
        return Response({'error': 'Calificación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    calificacion.delete()
    return Response({'mensaje': 'Calificación eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)