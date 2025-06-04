import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Crear el engine de SQLAlchemy para PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/uninorte")

# Leer datos con pandas usando el engine
df = pd.read_sql("SELECT * FROM libros_libro", con=engine)

# Mostrar resultados
print(df)

# Consulta SQL
query = """
SELECT 
    l.nombre AS libro,
    ROUND(AVG(c.puntaje)::numeric, 2) AS promedio,
    COUNT(c.id) AS cantidad
FROM libros_libro l
JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY l.nombre
ORDER BY promedio DESC
LIMIT 5;
"""

# Leer datos
df = pd.read_sql(query, con=engine)

# Calcular total y porcentaje
total_calificaciones = df['cantidad'].sum()
df['porcentaje'] = (df['cantidad'] / total_calificaciones * 100).round(1)

# Mostrar en consola
print("\nResumen de libros con mejor calificación promedio:\n")
for index, row in df.iterrows():
    print(f"- {row['libro']}: {row['promedio']} puntos, {row['cantidad']} calificaciones, {row['porcentaje']}% del total")

# Etiquetas X con porcentaje
labels = [f"{nombre}\n{porcentaje}%" for nombre, porcentaje in zip(df['libro'], df['porcentaje'])]

# Gráfico
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, df['promedio'], color='green')

# Texto encima de cada barra (cantidad de calificaciones)
for bar, cantidad in zip(bars, df['cantidad']):
    plt.text(bar.get_x() + bar.get_width() / 2, 
             bar.get_height() + 0.1, 
             f"{cantidad} calif.", 
             ha='center', va='bottom', fontsize=9, color='black')

# Estética
plt.title("Libros con mejor calificación promedio")
plt.ylabel("Puntaje promedio")
plt.xlabel("Libro (porcentaje de calificaciones)")
plt.ylim(0, 5.5)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Consulta SQL para promedio por usuario
query = """
SELECT
  u.username,
  AVG(c.puntaje) AS promedio
FROM
  auth_user u
JOIN
  libros_calificacion c ON c.user_id = u.id
GROUP BY
  u.username
ORDER BY
  promedio DESC;
"""

# Ejecutar la consulta y cargar en DataFrame
df_usuarios = pd.read_sql(query, con=engine)

# Mostrar el DataFrame en consola
print(df_usuarios)

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(df_usuarios['username'], df_usuarios['promedio'], color='skyblue')
plt.title('Promedio de Calificaciones por Usuario')
plt.xlabel('Usuario')
plt.ylabel('Puntaje Promedio')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 5)
plt.grid(axis='y')
plt.tight_layout()
plt.show()