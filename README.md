# Aplicacion Biblioteca Uninorte
Proyecto de Programación V

## Pasos para probar el proyecto

### Entorno Virtual
Se debe crear un entorno virtual con:

```bash
python -m venv venv
```

#### Librerias necesarias:
```Text
asgiref==3.8.1
contourpy==1.3.2
cycler==0.12.1
Django==5.2.1
django-extensions==4.1
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
fonttools==4.58.1
git-filter-repo==2.47.0
greenlet==3.2.2
kiwisolver==1.4.8
matplotlib==3.10.3
numpy==2.2.6
packaging==25.0
pandas==2.2.3
pillow==11.2.1
psycopg2-binary==2.9.10
PyJWT==2.9.0
pyparsing==3.2.3
python-dateutil==2.9.0.post0
python-decouple==3.8
pytz==2025.2
seaborn==0.13.2
six==1.17.0
SQLAlchemy==2.0.41
sqlparse==0.5.3
typing_extensions==4.14.0
tzdata==2025.2
```
#### Instalar las librerías
En el proyecto se genero un requirements.txt con:
```bash
pip freeze > requirements.txt
```
Se pueden instalar con:
```bash
pip install -r requirements.txt
```
### Crear la base de datos en PostgreSQL
Se puede crear en la interfaz de PGADMIN.

![Image](https://github.com/user-attachments/assets/3b98bd89-ad07-4316-b189-66a7ad451cd4)

Setear las credenciales en settings.py.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

```
En el proyecto, los datos sensibles estan protegidas con variables de entorno en .env (el cual esta en el gitignore, por eso no se sube al repositorio).

## API BIBLIOTECA - USOS
#### Explicación del Programa y Cómo Funciona
Esta API RESTful fue desarrollada utilizando Django y Django REST Framework. Su propósito principal es permitir la gestión de libros, géneros y autores, así como permitir a los usuarios registrar sus opiniones a través de calificaciones.

#### Funcionalidades principales
- Subida de libros: Los usuarios pueden crear nuevos libros indicando su título, género y autor.
- Gestión de autores y géneros: Se pueden registrar nuevos autores y géneros de forma dinámica.
- Sistema de calificaciones: Los usuarios autenticados pueden calificar los libros, permitiendo así generar valoraciones promedio.
- Registro de usuarios: El sistema permite registrar nuevos usuarios utilizando el modelo por defecto de Django (User), con una vista personalizada y un serializer que valida y crea los usuarios de forma segura.

## Prueba en Postman:

#### Registro:
```http
POST http://127.0.0.1:8000/api/auth/register/
```

El registro esta libre, cualquier usuario con la url puede registrarse sin un JWT.

```json
{
    "username": "prueba", 
    "password": "prueba123", 
    "email": "prueba@prueba.com"
}
```
![Image](https://github.com/user-attachments/assets/cc27bf65-8ec1-49b9-b9d6-6071bcb9ae2c)

#### Codigo para Registrar:

```Python
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permite el acceso sin autenticación

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Login:
```http
POST http://127.0.0.1:8000/api/auth/login/
```
```json
{
    "username": "prueba", 
    "password": "prueba123"
}
```

Ahi se genera el JWT, que luego debe usarse para autenticar las demás aplicaciones.

![Image](https://github.com/user-attachments/assets/4c62ec2c-e323-4570-80e3-72a7b4a9de61)


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
GET http://127.0.0.1:8000/api/autores/1/
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
PUT http://127.0.0.1:8000/api/autores/30/actualizar/
```
Se pasa el ID a actualizar en la URL y en el body los datos nuevos.

```Json
{ 
    "nombre": "Autor Prueba Modificado", 
    "nacionalidad": "Paraguaya" 
}
```

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

#### Eliminar Autor:
```http
DELETE http://127.0.0.1:8000/api/autores/30/eliminar
```
**Auth Type**: Bearer Token: el JWT generado.

Se pasa directamente el ID en la url para eliminar.

![Image](https://github.com/user-attachments/assets/ca55b03d-4218-4f53-a9fa-40f105524bc3)

#### Codigo para eliminar Autor:
```Python
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
POST http://127.0.0.1:8000/api/libros/crear/
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
#### Obtener Libro por ID:
```http
GET http://127.0.0.1:8000/api/libros/47/
```
**Auth Type**: Bearer Token: el JWT generado.

Se pasa directamente el ID en la url para obtener el libro.

![Image](https://github.com/user-attachments/assets/11f56445-7b64-49e7-9353-731baf94a336)

#### Codigo para obtener libro por ID:
```Python
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
```

#### Actualizar Libro
```http
PUT http://127.0.0.1:8000/api/libros/47/actualizar/
```
**Auth Type**: Bearer Token: el JWT generado.

Se pasa el ID del libro a actualizar y en el body se pasan los nuevos datos:
```Json
{
    "nombre": "Prueba Modificado",
    "fecha_lanzamiento": "2006-06-06",
    "url_libro": "https://pruebamodificado.net",
    "autor": 2,
    "genero": 2
}
```

![Image](https://github.com/user-attachments/assets/899905f7-d1a7-441a-b76b-78ea0c8af696)

#### Codigo para actualizar Libro:
```Python
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
```

#### Eliminar un Libro
```http
DELETE http://127.0.0.1:8000/api/libros/47/eliminar/
```
**Auth Type**: Bearer Token: el JWT generado.

Se pasa directamente el ID en la url para eliminar.

![Image](https://github.com/user-attachments/assets/09c4e312-e201-4136-a842-6af36a8012e7)

#### Codigo para eliminar Libro:

```Python
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
```

## Documentación del Script
Este script en Python está diseñado para conectarse a un proyecto Django y realizar análisis exploratorios de datos a partir de los registros y valoraciones disponibles en el sistema. Se utiliza principalmente para generar visualizaciones útiles para comprender mejor la información almacenada en las siguientes entidades del modelo:

- Autor
- Libro
- Calificación
- Género
- Usuario (User)

#### El script utiliza las siguientes bibliotecas principales:

- Django: Para acceder a los modelos y datos del ORM.
- pandas: Para convertir consultas en DataFrames y facilitar la manipulación de los datos.
- matplotlib.pyplot y seaborn: Para generar gráficos visualmente atractivos.

El acceso a los modelos se configura añadiendo el path raíz del proyecto y estableciendo la variable de entorno DJANGO_SETTINGS_MODULE. Luego, se inicializa Django para permitir la consulta de datos directamente desde los modelos.

#### Generación y Explicación de Gráficos
A continuación, se describen las funciones principales del script y los gráficos que genera:

#### promedio_calificaciones_por_genero()
Objetivo: Mostrar el promedio de calificaciones agrupadas por género literario.

Gráfico: Gráfico de barras.

Uso de pandas: Se convierte la consulta en un DataFrame para usarla con Seaborn.

![Image](https://github.com/user-attachments/assets/cbf292bf-5c9c-44b2-9354-ad9069073a3e)

#### top_autores_por_cantidad_libros()
Objetivo: Mostrar los 10 autores con más libros registrados.

Gráfico: Gráfico de barras.

Uso de pandas: Se usa para ordenar y graficar los datos con claridad.

![Image](https://github.com/user-attachments/assets/1068089b-553e-43df-bdb1-3cee67acd192)

#### distribucion_calificaciones()
Objetivo: Visualizar la distribución de puntajes otorgados en las calificaciones.

Gráfico: Histograma con curva KDE.

Uso de pandas: Se extraen los valores de calificaciones y se convierten en DataFrame.

![Image](https://github.com/user-attachments/assets/7b13c970-ba52-48fc-8067-57f021ea0eb0)

#### top_libros_por_cantidad_calificaciones()
Objetivo: Mostrar los libros con mayor cantidad de calificaciones.

Gráfico: Gráfico de barras.

![Image](https://github.com/user-attachments/assets/d0c1c144-1e95-43dd-ab2c-349e475c4dbd)

#### promedio_calificaciones_por_autor()
Objetivo: Calcular y visualizar el promedio de calificaciones por autor.

Gráfico: Gráfico de barras.

![Image](https://github.com/user-attachments/assets/70cf6ad9-8836-4e60-af8c-16f5ce887e30)

#### top_usuarios_por_calificaciones()
Objetivo: Identificar a los 10 usuarios que más calificaciones han realizado.

Gráfico: Gráfico de barras.

![Image](https://github.com/user-attachments/assets/7f7bcb66-c6ea-45aa-9cab-01b7deaee3ef)

### libros_sin_calificaciones()
Objetivo: Listar todos los libros que no tienen ninguna calificación asociada.

Salida: Se imprime un DataFrame con los nombres de los libros.

```bash
Libros sin calificaciones:
Empty DataFrame
Columns: []    
Index: []   
```
En la base de datos todos los libros tienen calificaciones.

#### top_libros_por_cantidad_y_promedio()
Objetivo: Mostrar los libros con al menos 5 calificaciones, ordenados por cantidad y calidad (promedio).

Gráfico: Scatter plot (diagrama de dispersión).

Uso de pandas: Para combinar cantidad y promedio en un gráfico informativo.

![Image](https://github.com/user-attachments/assets/1f7e2484-9a4d-4897-ab25-25b8ebad6dab)

#### distribucion_libros_por_anio()
Objetivo: Analizar la cantidad de libros lanzados por año.

Gráfico: Gráfico de línea.

Uso de ExtractYear: Para agrupar por año la fecha de lanzamiento.

![Image](https://github.com/user-attachments/assets/f6610903-1494-4064-b910-158e4e51fb2b)

#### boxplot_calificaciones_por_genero()
Objetivo: Mostrar la distribución de calificaciones (mínimos, máximos, medianas, etc.) por género.

Gráfico: Diagrama de caja (boxplot).

Uso de pandas: Para transformar y renombrar columnas de datos relacionados.

![Image](https://github.com/user-attachments/assets/1885e00f-0abc-46a5-9900-e3c5dbccac38)

#### top_generos_por_cantidad_libros()
Objetivo: Identificar los géneros con más libros registrados.

Gráfico: Gráfico de barras.

![Image](https://github.com/user-attachments/assets/94565349-453f-4e13-85e4-ec5acdecb8ff)

#### ¿Por qué usamos pandas?
La librería pandas es fundamental para este script porque:

- Permite transformar consultas complejas de Django ORM en estructuras tipo tabla (DataFrames).
- Facilita la limpieza, agrupamiento y ordenamiento de los datos antes de graficarlos.
- Es compatible directamente con Seaborn y Matplotlib, haciendo el flujo de análisis y visualización mucho más fluido.


## Licencia

Este proyecto está licenciado bajo los términos de la **Licencia MIT**.

Puedes usar, copiar, modificar y distribuir este software con o sin fines comerciales, siempre que mantengas el aviso de copyright original y esta licencia.


### Bibliotecas de terceros

Este proyecto utiliza las siguientes bibliotecas de código abierto, cada una sujeta a sus propias licencias:

- **Django** (BSD License)
- **djangorestframework** (BSD License)
- **djangorestframework_simplejwt** (MIT License)
- **pandas** (BSD License)
- **matplotlib** (PSF License)
- **seaborn** (BSD License)
- **numpy** (BSD License)
- **SQLAlchemy** (MIT License)
- **python-decouple**, **pillow**, **psycopg2-binary**, **PyJWT**, entre otras.

Consulta la documentación oficial de cada paquete para más detalles sobre sus licencias.
