from django.core.management.base import BaseCommand
from libros.models import Genero, Libro
from django.db.models import Count, Avg

class Command(BaseCommand):
    help = 'Sistema de recomendación de géneros por cantidad de calificaciones'

    def handle(self, *args, **options):
        while True:
            generos = list(Genero.objects.all())
            if not generos:
                self.stdout.write(self.style.ERROR('No hay géneros registrados.'))
                break

            self.stdout.write('\nSistema de Recomendación de Géneros:')
            for idx, genero in enumerate(generos, 1):
                self.stdout.write(f"{idx} - {genero.nombre}")
            self.stdout.write(f"{len(generos)+1} - Salir\n")

            try:
                seleccion = int(input('Seleccione el género: '))
            except ValueError:
                self.stdout.write(self.style.WARNING('Por favor, ingrese un número válido.'))
                continue

            if seleccion == len(generos) + 1:
                self.stdout.write(self.style.SUCCESS('¡Hasta luego!'))
                break

            if not (1 <= seleccion <= len(generos)):
                self.stdout.write(self.style.WARNING('Selección fuera de rango.'))
                continue

            genero = generos[seleccion - 1]
            self.mostrar_recomendaciones_genero(genero)

    def mostrar_recomendaciones_genero(self, genero):
        self.stdout.write(self.style.SUCCESS(
            f'\nLibros recomendados para el género: {genero.nombre}\n'
        ))

        libros = (
            Libro.objects
            .filter(genero=genero)
            .annotate(
                cantidad_calificaciones=Count('calificaciones'),
                promedio_calificaciones=Avg('calificaciones__puntaje')
            )
            .order_by('-cantidad_calificaciones', '-promedio_calificaciones')
        )

        if not libros:
            self.stdout.write('No hay libros con calificaciones en este género.\n')
            return

        for idx, libro in enumerate(libros, 1):
            self.stdout.write(
                f"{idx}. {libro.nombre} | "
                f"Calificaciones: {libro.cantidad_calificaciones} | "
                f"Promedio: {libro.promedio_calificaciones:.2f}" if libro.promedio_calificaciones is not None else "Sin calificaciones"
            )
        self.stdout.write("")  # Línea en blanco al final
