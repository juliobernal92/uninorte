import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import sys

# Añade la ruta raíz de tu proyecto Django al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Establece la variable de entorno para que Django sepa dónde está la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uninorte.settings')

import django
django.setup()
from libros.models import Autor, Libro, Calificacion, Genero
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce


def promedio_calificaciones_por_genero():
    qs = Genero.objects.annotate(
        promedio=Avg('libros__calificaciones__puntaje')
    ).order_by('-promedio').values('nombre', 'promedio')[:10]

    df = pd.DataFrame(list(qs))

    plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='nombre', y='promedio', hue='nombre', palette='Blues_d')
    plt.title("Promedio de calificaciones por género")
    plt.xlabel("Género")
    plt.ylabel("Promedio puntaje")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def top_autores_por_cantidad_libros():
    qs = Autor.objects.annotate(
        cantidad_libros=Count('libros')
    ).order_by('-cantidad_libros').values('nombre', 'cantidad_libros')[:10]

    df = pd.DataFrame(list(qs))
    plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='nombre', y='cantidad_libros',hue='nombre', palette='Oranges_d')
    plt.title("Top 10 autores por número de libros")
    plt.xlabel("Autor")
    plt.ylabel("Cantidad de libros")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def distribucion_calificaciones():
    qs = Calificacion.objects.values_list('puntaje', flat=True)
    df = pd.DataFrame(qs, columns=['puntaje'])

    plt.figure(figsize=(8,4))
    sns.histplot(df['puntaje'], bins=20, kde=True, color='skyblue')
    plt.title("Distribución de calificaciones")
    plt.xlabel("Puntaje")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()


def top_libros_por_cantidad_calificaciones():
    qs = Libro.objects.annotate(
        cantidad_calificaciones=Count('calificaciones')
    ).order_by('-cantidad_calificaciones').values('nombre', 'cantidad_calificaciones')[:10]

    df = pd.DataFrame(list(qs))
    plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='nombre', y='cantidad_calificaciones', hue='nombre', palette='Greens_d')
    plt.title("Top 10 libros por cantidad de calificaciones")
    plt.xlabel("Libro")
    plt.ylabel("Cantidad de calificaciones")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def promedio_calificaciones_por_autor():
    qs = Autor.objects.annotate(
        promedio=Avg('libros__calificaciones__puntaje')
    ).order_by('-promedio').values('nombre', 'promedio')[:10]

    df = pd.DataFrame(list(qs))
    plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='nombre', y='promedio', hue='nombre',  palette='Reds_d')
    plt.title("Promedio de calificaciones por autor")
    plt.xlabel("Autor")
    plt.ylabel("Promedio puntaje")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def top_usuarios_por_calificaciones():
    qs = User.objects.annotate(
        cantidad_calificaciones=Count('calificacion')
    ).order_by('-cantidad_calificaciones').values('username', 'cantidad_calificaciones')[:10]

    df = pd.DataFrame(list(qs))
    plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='username', y='cantidad_calificaciones', color='saddlebrown')
    plt.title("Top 10 usuarios por cantidad de calificaciones")
    plt.xlabel("Usuario")
    plt.ylabel("Cantidad de calificaciones")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def libros_sin_calificaciones():
    qs = Libro.objects.annotate(
        cantidad_calificaciones=Count('calificaciones')
    ).filter(cantidad_calificaciones=0).order_by('nombre').values('nombre')

    df = pd.DataFrame(list(qs))
    print("Libros sin calificaciones:")
    print(df)


def top_libros_por_cantidad_y_promedio():
    qs = Libro.objects.annotate(
        cantidad_calificaciones=Count('calificaciones'),
        promedio=Avg('calificaciones__puntaje')
    ).filter(cantidad_calificaciones__gte=5).order_by('-cantidad_calificaciones', '-promedio').values('nombre', 'cantidad_calificaciones', 'promedio')[:20]

    df = pd.DataFrame(list(qs))

    plt.figure(figsize=(12,6))
    sns.scatterplot(data=df, x='cantidad_calificaciones', y='promedio', color='darkcyan', s=100)

    for i, row in df.iterrows():
        plt.text(row['cantidad_calificaciones']+0.1, row['promedio']-0.05, row['nombre'], fontsize=8)

    plt.title("Top libros por cantidad y promedio de calificaciones")
    plt.xlabel("Cantidad de calificaciones")
    plt.ylabel("Promedio de puntaje")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def top_generos_por_cantidad_libros():
    qs = Genero.objects.annotate(
        cantidad_libros=Count('libros')
    ).order_by('-cantidad_libros').values('nombre', 'cantidad_libros')[:10]

    df = pd.DataFrame(list(qs))

    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x='nombre', y='cantidad_libros', hue='nombre', palette='Purples_d', legend=False)
    plt.title("Top 10 géneros por cantidad de libros")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de libros")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def boxplot_calificaciones_por_genero():
    qs = Calificacion.objects.select_related('libro__genero').values(
        'libro__genero__nombre', 'puntaje'
    )

    df = pd.DataFrame(list(qs))
    df.rename(columns={'libro__genero__nombre': 'genero'}, inplace=True)

    plt.figure(figsize=(12,6))
    sns.boxplot(data=df, x='genero', y='puntaje', hue='genero',  palette='coolwarm')
    plt.title("Distribución de calificaciones por género (Boxplot)")
    plt.xlabel("Género")
    plt.ylabel("Puntaje")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


from django.db.models.functions import ExtractYear

def distribucion_libros_por_anio():
    qs = Libro.objects.annotate(
        anio=ExtractYear('fecha_lanzamiento')
    ).values('anio').annotate(
        cantidad=Count('id')
    ).order_by('anio')

    df = pd.DataFrame(list(qs))

    plt.figure(figsize=(10,5))
    sns.lineplot(data=df, x='anio', y='cantidad', marker='o', color='teal')
    plt.title("Distribución de libros por año de lanzamiento")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de libros")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import django
    django.setup()

    promedio_calificaciones_por_genero()
    top_autores_por_cantidad_libros()
    distribucion_calificaciones()
    top_libros_por_cantidad_calificaciones()
    promedio_calificaciones_por_autor()
    top_usuarios_por_calificaciones()
    libros_sin_calificaciones()
    top_libros_por_cantidad_y_promedio()
    distribucion_libros_por_anio()
    boxplot_calificaciones_por_genero()
    top_generos_por_cantidad_libros()
    
