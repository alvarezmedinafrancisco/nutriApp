from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.secret_key = "12345" 


API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
API_KEY = "P7OwftVfyTrK3P0YbAbobV2JMY0HEYcvWUOY4tYm"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


        
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

@app.route("/tmb" , methods=['GET', 'POST'])
def tmb():
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])
        sexo = request.form['sexo']
        if sexo == 'hombre':
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura * 100) - (5.7 * edad)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura * 100) - (4.3 * edad)
        return render_template("tmb.html", tmb=tmb)
    return render_template("tmb.html")

@app.route("/gct", methods=['GET', 'POST'])
def gct():
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        nivel_actividad = request.form['actividad']
        factores_actividad = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muy_intenso': 1.9
        }
        gct = tmb * factores_actividad.get(nivel_actividad, 1.2)
        return render_template("gct.html", gct=gct)
    return render_template("gct.html")

@app.route("/macro", methods=['GET', 'POST'])
def macro():
    if request.method == 'POST':
        gct = float(request.form['gct'])
        objetivo = request.form['objetivo']
        if objetivo == 'perder':
            calorias = gct - 500
        elif objetivo == 'ganar':
            calorias = gct + 500
        else:
            calorias = gct
        proteinas = calorias * 0.3 / 4
        grasas = calorias * 0.25 / 9
        carbohidratos = calorias * 0.45 / 4
        return render_template("macro.html", calorias=calorias, proteinas=proteinas, grasas=grasas, carbos=carbohidratos)
    return render_template("macro.html")


@app.route("/pesoideal", methods=['GET', 'POST'])
def peso_ideal():
    if request.method == 'POST':
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        if sexo == 'hombre':
            peso_ideal = 50 + 2.3 * ((altura * 100 / 2.54) - 60)
        else:
            peso_ideal = 45.5 + 2.3 * ((altura * 100 / 2.54) - 60)
        return render_template("peso_ideal.html", peso_ideal=peso_ideal)
    return render_template("peso_ideal.html")

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
