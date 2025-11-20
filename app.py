from flask import Flask,render_template , request , url_for
app = Flask(__name__)

@app.route('/')
def index():
    usuario = [{"name : pepe",
                "apellidos : pica piedra",
                "edad : 26",
                "sexo : masculino",
                "peso : 88",
                "altura : 1.88",
                "nivel de actividad fisica : Moderado",
                "correo electronico : pepe@gmail.com",
                "contra : pepe123",
                "objetivo : bajar de peso",
                "nivel de cosima : master chef",
                "preferencias alimenticias : Keto",
                "Alergias alimentarias : nada"
                }]
    return render_template('registrate.html')

@app.route("/base")
def base():
    return render_template("base.html")


@app.route('/info' , methods=['GET', 'POST'])
def info():
    return render_template('info.html') 

@app.route("/recetas")
def recetas():
    return render_template("recetas.html")

@app.route("/calculadora")
def calcula():
    return render_template("/calcula.html")

@app.route("/recomendaciones")
def recomendaciones():
    return render_template("/recomendaciones.html")

@app.route("/registrate" , methods=['GET', 'POST'])
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
        return render_template("/perfil.html", nombre=nombre)
    return render_template("/registrate.html")

@app.route("/utiles", methods=['GET', 'POST'])
def utiles():
    if request.method == 'POST':
        peso = request.form['peso']
        altura = request.form['altura']
        edad = request.form['edad']
        sexo = request.form['sexo']
        nivel_actividad = request.form['nivel_actividad']

        try:
            peso = float(peso)
            altura = float(altura)
            edad = int(edad)
        except (TypeError, ValueError):
            return render_template("utiles.html", error="Entrada inválida")
        imc = peso / (altura * altura) if altura > 0 else None


        altura_cm = altura * 100
        if str(sexo).lower() == 'masculino':
            tmb = 10 * peso + 6.25 * altura_cm - 5 * edad + 5
        else:
            tmb = 10 * peso + 6.25 * altura_cm - 5 * edad - 161

        activity_factors = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'activo': 1.725,
            'muy_activo': 1.9
        }
        factor = activity_factors.get(nivel_actividad, 1.2)
        gct = tmb * factor

        ideal = 22 * (altura * altura)

        macro = {
            'proteinas': (gct * 0.2) / 4,
            'carbos': (gct * 0.5) / 4,
            'grasas': (gct * 0.3) / 9
        }

        return render_template("utiles.html", imc=imc, tmb=tmb, gct=gct, ideal=ideal, macro=macro)

    return render_template("utiles.html")

@app.route("/perfil")
def perfil():
    return render_template("/perfil.html")  

if __name__ == '__main__':
    app.run(debug=True)