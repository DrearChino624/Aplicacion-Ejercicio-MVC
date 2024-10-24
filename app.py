from flask import Flask, render_template, request
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="gestion_jugadores"  # Cambiado a la nueva base de datos
)

cursor = db.cursor()

# Función para crear la base de datos y la tabla con datos quemados
def create_database_and_table():
    cursor.execute("DROP DATABASE IF EXISTS gestion_jugadores;")
    cursor.execute("CREATE DATABASE IF NOT EXISTS gestion_jugadores;")
    cursor.execute("USE gestion_jugadores;")
    
    # Crear tabla jugadores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jugadores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_jugador VARCHAR(255) NOT NULL,
        fecha_ultimo_encuentro DATE NOT NULL,
        goles_ultimo_encuentro INT NOT NULL,
        estado VARCHAR(50) NOT NULL,
        equipo VARCHAR(255) NOT NULL,
        promedio_goles FLOAT NOT NULL
    );
    """)

    # Insertar datos quemados
    cursor.execute("""
    INSERT INTO jugadores (id, nombre_jugador, fecha_ultimo_encuentro, goles_ultimo_encuentro, estado, equipo, promedio_goles)
    VALUES
    (1, 'Lionel Messi', '2024-10-15', 2, 'Activo', 'Inter Miami', 0.87),
    (2, 'Cristiano Ronaldo', '2024-09-30', 1, 'Activo', 'Al-Nassr', 0.75),
    (3, 'Zlatan Ibrahimović', '2023-05-20', 0, 'Retirado', 'AC Milan', 0.68),
    (4, 'Neymar Jr.', '2024-08-25', 1, 'Activo', 'Al-Hilal', 0.65),
    (5, 'Andrés Iniesta', '2023-06-15', 0, 'Retirado', 'Vissel Kobe', 0.1);
    """)
    
    # Confirmar los cambios
    db.commit()

# Llama a la función para crear la base de datos y tabla
create_database_and_table()

@app.route('/')
def index():
    # Consulta todos los jugadores de la base de datos
    cursor.execute("SELECT * FROM jugadores")
    jugadores = cursor.fetchall()
    return render_template('index.html', jugadores=jugadores)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_jugadores():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        query = "SELECT * FROM jugadores WHERE estado = 'Activo' AND fecha_ultimo_encuentro BETWEEN %s AND %s"
        cursor.execute(query, (fecha_inicio, fecha_fin))
        jugadores = cursor.fetchall()

        jugadores_con_estadisticas = []

        # Calcular el promedio de goles de los jugadores en el rango de fechas
        for jugador in jugadores:
            id_jugador = jugador[0]
            nombre = jugador[1]
            fecha_ultimo_encuentro = jugador[2]
            goles_ultimo_encuentro = jugador[3]
            estado = jugador[4]
            equipo = jugador[5]
            promedio_goles = jugador[6]

            # Si hay algún cálculo extra, puedes agregarlo aquí. Por ahora, solo se toman los datos existentes.
            jugador_con_estadisticas = (id_jugador, nombre, fecha_ultimo_encuentro, goles_ultimo_encuentro, estado, equipo, promedio_goles)
            jugadores_con_estadisticas.append(jugador_con_estadisticas)

        return render_template('index.html', jugadores=jugadores_con_estadisticas)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
