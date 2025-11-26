from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.secret_key = "12345" 


API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "1YeHW5ssRNnnsULz2f3nq5ZNYtQWfJYHlbtUwtyQ"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'averquerollo'


        
@app.route('/')
def index():    
    return render_template('registrate.html')

@app.route("/foods", methods=['GET', 'POST'])
def get_foods():
    food_name = request.args.get("food_name", "").strip()
    if not food_name:
        food_name = "apple"
    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 12
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        foods = data.get("foods", [])
        return render_template("foods.html", foods=foods, food_name=food_name, error=None)
    except requests.exceptions.RequestException as e:
        error_message = f"Ocurrió un error al consultar la API: {e}"
        return render_template("foods.html", foods=[], food_name=food_name, error=error_message)


@app.route("/imc" , methods=['GET', 'POST'])
def imc():
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = peso / (altura * altura)
        return render_template("imc.html", imc=imc)
    return render_template("imc.html")

mysql = MySQL(app)
def email_exists(correo):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None

@app.route("/registrate", methods=['GET', 'POST'])
def registrate():
    if request.method == 'POST':

        nombre = request.form['name']
        apellidos = request.form['apellidos']
        edad = request.form['edad']
        sexo = request.form['sexo']
        peso = request.form['peso']
        altura = request.form['altura']
        nivel_actividad = request.form['nivel_actividad']
        correo = request.form['email']
        contra = request.form['contra']
        objetivo = request.form['objetivo']
        nivel_cocina = request.form['nivel_cocina']
        preferencias = request.form['preferencias']
        alergias = request.form['alergias']
        if email_exists(correo):
            flash("Ese correo ya está registrado, elige otro.")
            return redirect(url_for('registrate'))

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO usuarios 
            (nombre, apellidos, edad, sexo, peso, altura, nivel_actividad, correo, contra, objetivo, nivel_cocina, preferencias, alergias)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, apellidos, edad, sexo, peso, altura, nivel_actividad, correo, contra, objetivo, nivel_cocina, preferencias, alergias))

        mysql.connection.commit()
        cursor.close()

        flash("Usuario registrado correctamente.")
        return redirect(url_for('perfil', nombre=nombre))

    return render_template("registrate.html")
@app.route("/perfil")
def perfil():
    nombre = request.args.get('nombre', 'Usuario')
    return render_template("perfil.html", nombre=nombre)
@app.route("/base")
def base():
    return render_template("base.html")
@app.route("/info")
def info():
    return render_template("info.html")
@app.route("/recetas")
def recetas():
    return render_template("recetas.html")
@app.route("/calculadora")
def calcula():
    return render_template("calcula.html")
@app.route("/recomendaciones")
def recomendaciones():
    return render_template("recomendaciones.html")
@app.route("/utiles")
def utiles():
    return render_template("utiles.html")

if __name__ == '__main__':
    app.run(debug=True)
