import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Crear el engine de SQLAlchemy para PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/uninorte")

# Leer datos con pandas usando el engine
df = pd.read_sql("SELECT * FROM libros_libro", con=engine)

#Promedio de calificaciones por género
query = """
SELECT g.nombre AS genero, AVG(c.puntaje) AS promedio
FROM libros_genero g
JOIN libros_libro l ON l.genero_id = g.id
JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY g.nombre
ORDER BY promedio DESC;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["genero"], df["promedio"], color='purple')
plt.title("Promedio de calificaciones por género")
plt.xlabel("Género")
plt.ylabel("Promedio puntaje")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#2. Número de libros por autor
query = """
SELECT a.nombre AS autor, COUNT(l.id) AS cantidad_libros
FROM libros_autor a
LEFT JOIN libros_libro l ON l.autor_id = a.id
GROUP BY a.nombre
ORDER BY cantidad_libros DESC
LIMIT 10;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["autor"], df["cantidad_libros"], color='orange')
plt.title("Top 10 autores por número de libros")
plt.xlabel("Autor")
plt.ylabel("Cantidad de libros")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#3. Distribución de calificaciones (histograma)
query = "SELECT puntaje FROM libros_calificacion;"
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(8,4))
plt.hist(df["puntaje"], bins=20, color='skyblue', edgecolor='black')
plt.title("Distribución de calificaciones")
plt.xlabel("Puntaje")
plt.ylabel("Frecuencia")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#4. Cantidad de calificaciones por libro
query = """
SELECT l.nombre AS libro, COUNT(c.id) AS cantidad_calificaciones
FROM libros_libro l
LEFT JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY l.nombre
ORDER BY cantidad_calificaciones DESC
LIMIT 10;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["libro"], df["cantidad_calificaciones"], color='green')
plt.title("Top 10 libros por cantidad de calificaciones")
plt.xlabel("Libro")
plt.ylabel("Cantidad de calificaciones")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#4. Cantidad de calificaciones por libro
query = """
SELECT l.nombre AS libro, COUNT(c.id) AS cantidad_calificaciones
FROM libros_libro l
LEFT JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY l.nombre
ORDER BY cantidad_calificaciones DESC
LIMIT 10;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["libro"], df["cantidad_calificaciones"], color='green')
plt.title("Top 10 libros por cantidad de calificaciones")
plt.xlabel("Libro")
plt.ylabel("Cantidad de calificaciones")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#Calificaciones promedio por autor
query = """
SELECT a.nombre AS autor, AVG(c.puntaje) AS promedio
FROM libros_autor a
JOIN libros_libro l ON l.autor_id = a.id
JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY a.nombre
ORDER BY promedio DESC
LIMIT 10;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["autor"], df["promedio"], color='red')
plt.title("Promedio de calificaciones por autor")
plt.xlabel("Autor")
plt.ylabel("Promedio puntaje")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()


#6. Usuarios con más calificaciones
query = """
SELECT u.username, COUNT(c.id) AS cantidad_calificaciones
FROM auth_user u
JOIN libros_calificacion c ON c.user_id = u.id
GROUP BY u.username
ORDER BY cantidad_calificaciones DESC
LIMIT 10;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,5))
plt.bar(df["username"], df["cantidad_calificaciones"], color='brown')
plt.title("Top 10 usuarios por cantidad de calificaciones")
plt.xlabel("Usuario")
plt.ylabel("Cantidad de calificaciones")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#8. Libros sin calificaciones
query = """
SELECT l.nombre, COUNT(c.id) AS cantidad_calificaciones
FROM libros_libro l
LEFT JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY l.nombre
HAVING COUNT(c.id) = 0
ORDER BY l.nombre;
"""
df = pd.read_sql(query, con=engine)

print("Libros sin calificaciones:")
print(df)


#9. Top libros por cantidad de calificaciones y promedio (scatter plot)
query = """
SELECT l.nombre, COUNT(c.id) AS cantidad_calificaciones, AVG(c.puntaje) AS promedio
FROM libros_libro l
JOIN libros_calificacion c ON c.libro_id = l.id
GROUP BY l.nombre
HAVING COUNT(c.id) >= 5
ORDER BY cantidad_calificaciones DESC, promedio DESC
LIMIT 20;
"""
df = pd.read_sql(query, con=engine)

plt.figure(figsize=(10,6))
plt.scatter(df["cantidad_calificaciones"], df["promedio"], color='darkcyan')
for i, txt in enumerate(df["nombre"]):
    plt.annotate(txt, (df["cantidad_calificaciones"][i], df["promedio"][i]),
                 textcoords="offset points", xytext=(5,-10), ha='left', fontsize=8)
plt.title("Top libros por cantidad y promedio de calificaciones")
plt.xlabel("Cantidad de calificaciones")
plt.ylabel("Promedio de puntaje")
plt.grid(True)
plt.tight_layout()
plt.show()



