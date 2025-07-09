from django.core.management.base import BaseCommand
from libros.models import Autor, Libro, Calificacion, Genero
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce, ExtractYear
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

CARPETA_REPORTE = 'reportes'

class Command(BaseCommand):
    help = 'Genera y guarda reportes gráficos y de consola sobre libros, autores, géneros y calificaciones.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--solo',
            type=str,
            help='Ejecuta solo el reporte especificado (nombre del método sin paréntesis, ej: promedio_calificaciones_por_genero)'
        )

    def handle(self, *args, **options):
        if not os.path.exists(CARPETA_REPORTE):
            os.makedirs(CARPETA_REPORTE)

        # Lista de (nombre_función, nombre_archivo, descripción) para el orden y nombres de los archivos
        reportes = [
            ('promedio_calificaciones_por_genero',        '01_promedio_calificaciones_por_genero.png',        "Promedio de calificaciones por género"),
            ('top_autores_por_cantidad_libros',           '02_top_autores_por_cantidad_libros.png',           "Top autores por cantidad de libros"),
            ('distribucion_calificaciones',               '03_distribucion_calificaciones.png',               "Distribución de calificaciones"),
            ('top_libros_por_cantidad_calificaciones',    '04_top_libros_por_cantidad_calificaciones.png',    "Top libros por cantidad de calificaciones"),
            ('promedio_calificaciones_por_autor',         '05_promedio_calificaciones_por_autor.png',         "Promedio de calificaciones por autor"),
            ('top_usuarios_por_calificaciones',           '06_top_usuarios_por_calificaciones.png',           "Top usuarios por cantidad de calificaciones"),
            ('libros_sin_calificaciones',                 None,                                               "Libros sin calificaciones"),  # Solo imprime en consola
            ('top_libros_por_cantidad_y_promedio',        '07_top_libros_por_cantidad_y_promedio.png',        "Top libros por cantidad y promedio de calificaciones"),
            ('distribucion_libros_por_anio',              '08_distribucion_libros_por_anio.png',              "Distribución de libros por año de lanzamiento"),
            ('boxplot_calificaciones_por_genero',         '09_boxplot_calificaciones_por_genero.png',         "Boxplot calificaciones por género"),
            ('top_generos_por_cantidad_libros',           '10_top_generos_por_cantidad_libros.png',           "Top géneros por cantidad de libros"),
        ]

        solo = options.get('solo')
        metodos = {r[0]: r for r in reportes}

        if solo:
            if solo in metodos:
                self.stdout.write(self.style.SUCCESS(f'\n---- Ejecutando: {solo} ----'))
                self._ejecutar_reporte(*metodos[solo])
            else:
                self.stdout.write(self.style.ERROR(
                    f'No existe el reporte "{solo}". Usa uno de: {", ".join(metodos.keys())}'
                ))
            return

        # Ejecuta todos los reportes
        for nombre_func, nombre_archivo, desc in reportes:
            self.stdout.write(self.style.SUCCESS(f'\n---- Ejecutando: {desc} ----'))
            self._ejecutar_reporte(nombre_func, nombre_archivo, desc)

    def _ejecutar_reporte(self, nombre_func, nombre_archivo, desc):
        if hasattr(self, nombre_func):
            metodo = getattr(self, nombre_func)
            if nombre_archivo:
                metodo(nombre_archivo)
            else:
                metodo()
        else:
            self.stdout.write(self.style.ERROR(f'No se encuentra la función {nombre_func}'))

    # ========== REPORTE 1 ==========
    def promedio_calificaciones_por_genero(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 2 ==========
    def top_autores_por_cantidad_libros(self, nombre_archivo):
        qs = Autor.objects.annotate(
            cantidad_libros=Count('libros')
        ).order_by('-cantidad_libros').values('nombre', 'cantidad_libros')[:10]

        df = pd.DataFrame(list(qs))
        plt.figure(figsize=(10,5))
        sns.barplot(data=df, x='nombre', y='cantidad_libros', hue='nombre', palette='Oranges_d')
        plt.title("Top 10 autores por número de libros")
        plt.xlabel("Autor")
        plt.ylabel("Cantidad de libros")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 3 ==========
    def distribucion_calificaciones(self, nombre_archivo):
        qs = Calificacion.objects.values_list('puntaje', flat=True)
        df = pd.DataFrame(qs, columns=['puntaje'])

        plt.figure(figsize=(8,4))
        sns.histplot(df['puntaje'], bins=20, kde=True, color='skyblue')
        plt.title("Distribución de calificaciones")
        plt.xlabel("Puntaje")
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 4 ==========
    def top_libros_por_cantidad_calificaciones(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 5 ==========
    def promedio_calificaciones_por_autor(self, nombre_archivo):
        qs = Autor.objects.annotate(
            promedio=Avg('libros__calificaciones__puntaje')
        ).order_by('-promedio').values('nombre', 'promedio')[:10]

        df = pd.DataFrame(list(qs))
        plt.figure(figsize=(10,5))
        sns.barplot(data=df, x='nombre', y='promedio', hue='nombre', palette='Reds_d')
        plt.title("Promedio de calificaciones por autor")
        plt.xlabel("Autor")
        plt.ylabel("Promedio puntaje")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 6 ==========
    def top_usuarios_por_calificaciones(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 7 ==========
    def libros_sin_calificaciones(self):
        qs = Libro.objects.annotate(
            cantidad_calificaciones=Count('calificaciones')
        ).filter(cantidad_calificaciones=0).order_by('nombre').values('nombre')

        df = pd.DataFrame(list(qs))
        self.stdout.write("Libros sin calificaciones:")
        if not df.empty:
            self.stdout.write(df.to_string(index=False))
        else:
            self.stdout.write("No hay libros sin calificaciones.")

    # ========== REPORTE 8 ==========
    def top_libros_por_cantidad_y_promedio(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 9 ==========
    def distribucion_libros_por_anio(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 10 ==========
    def boxplot_calificaciones_por_genero(self, nombre_archivo):
        qs = Calificacion.objects.select_related('libro__genero').values(
            'libro__genero__nombre', 'puntaje'
        )

        df = pd.DataFrame(list(qs))
        df.rename(columns={'libro__genero__nombre': 'genero'}, inplace=True)

        plt.figure(figsize=(12,6))
        sns.boxplot(data=df, x='genero', y='puntaje', hue='genero', palette='coolwarm')
        plt.title("Distribución de calificaciones por género (Boxplot)")
        plt.xlabel("Género")
        plt.ylabel("Puntaje")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()

    # ========== REPORTE 11 ==========
    def top_generos_por_cantidad_libros(self, nombre_archivo):
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
        plt.savefig(os.path.join(CARPETA_REPORTE, nombre_archivo))
        plt.show()
        plt.close()
