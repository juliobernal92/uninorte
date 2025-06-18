# Uninorte
Proyecto de Programación V

## Pasos para probar el proyecto

### Instalar las librerías
```bash
pip install -r requirements.txt
```

### Crear la base de datos en PostgreSQL
Setear las credenciales.

### Prueba en Postman:

#### Registro:
```http
POST http://127.0.0.1:8000/api/auth/register/
```
```json
{
  "username": "usuario",
  "password": "contrasenha",
  "email": "usuario@example.com"
}
```

#### Login:
```http
POST http://127.0.0.1:8000/api/auth/login/
```
```json
{
  "username": "usuario",
  "password": "contrasenha"
}
```

Ahi se genera el JWT, que luego debe usarse para las demás aplicaciones.

### AUTORES:

#### Obtener Todos:
```http
GET http://127.0.0.1:8000/api/autores/
```
**Auth Type**: Bearer Token: el JWT generado.


![Image](https://github.com/user-attachments/assets/20b35682-f0f7-4ba9-a282-07b3715971e4)

#### Codigo para Obtener Todos los Autores:
```Python
# Listar autores
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_autores(request):
    autores = Autor.objects.all()
    serializer = AutorSerializer(autores, many=True)
    return Response(serializer.data)
```

#### Insertar Autor:
```http
POST http://127.0.0.1:8000/api/autores/crear/
```
```json
{ 
    "nombre": "Autor Prueba", 
    "nacionalidad": "Paraguaya" 
}
```
**Auth Type**: Bearer Token: el JWT generado.

![Image](https://github.com/user-attachments/assets/5ede8ac8-3eb0-4d2c-b2e3-12dc562e4769)

#### Codigo para insertar un Autor:
```Python
# Crear autor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_autor(request):
    serializer = AutorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Obtener Autor por ID
```http
POST http://127.0.0.1:8000/api/autores/1/
```
Se pasa el ID a buscar en la url directamente.

**Auth Type**: Bearer Token: el JWT generado.

![Image](https://github.com/user-attachments/assets/08e6a4b4-3c08-4585-97ff-e27b6baa0166)

#### Codigo para obtener Autor por ID:
```Python
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
```

#### Actualizar Autor
```http
PUT http://127.0.0.1:8000/api/autores/1/actualizar/
```
Se pasa el ID a actualizar en la URL.

**Auth Type**: Bearer Token: el JWT generado.

![Image](https://github.com/user-attachments/assets/ff547574-aefe-41b0-b88b-369234db0847)

#### Codigo para Actualizar:
```Python
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
```

### LIBROS:

#### Obtener Todos los libros:
```http
GET http://127.0.0.1:8000/api/libros/
```
**Auth Type**: Bearer Token: el JWT generado.

![Image](https://github.com/user-attachments/assets/bfcfee25-c2d0-4afe-b16d-b47c0132a8c7)

#### Codigo para obtener todos los libros:
```Python
# Listar libros
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_libros(request):
    libros = Libro.objects.all()
    serializer = LibroSerializer(libros, many=True)
    return Response(serializer.data)
```

#### Insertar Libros
```http
GET http://127.0.0.1:8000/api/libros/crear/
```
**Auth Type**: Bearer Token: el JWT generado.

![Image](https://github.com/user-attachments/assets/5318a3b6-ea9a-455a-8e5f-e05f59b01610)

#### Codigo para insertar libros:
```Python
# Crear Libro
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_libro(request):
    serializer = LibroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
