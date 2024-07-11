from flask import Flask, render_template, request
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_tareas"
)

cursor = db.cursor()

@app.route('/')
def index():
    # Consulta todas las tareas de la base de datos
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    return render_template('index.html', tareas=tareas)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_tareas():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        query = "SELECT * FROM tareas WHERE estado = 'En progreso' AND fecha BETWEEN %s AND %s"
        cursor.execute(query, (fecha_inicio, fecha_fin))
        tareas = cursor.fetchall()

        tareas_con_retraso = []

        # Calcular el retraso de cada tarea
        for tarea in tareas:
            id_tarea = tarea[0]
            nombre = tarea[1]
            fecha_tarea = tarea[2]
            tiempo_estimado = tarea[3]
            estado = tarea[4]
            encargado = tarea[5]

            # Calcular la fecha de fin estimada
            fecha_fin_estimada = fecha_tarea + timedelta(days=tiempo_estimado)

            # Calcular el tiempo de retraso
            if datetime.now().date() > fecha_fin_estimada:
                dias_retraso = (datetime.now().date() - fecha_fin_estimada).days
            else:
                dias_retraso = 0

            # Agregar el tiempo de retraso a la tarea
            tarea_con_retraso = (id_tarea, nombre, fecha_tarea, tiempo_estimado, estado, encargado, dias_retraso)
            tareas_con_retraso.append(tarea_con_retraso)

        return render_template('index.html', tareas=tareas_con_retraso)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)