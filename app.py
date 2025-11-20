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

@app.route("/utiles")
def utiles():
    return render_template("/utiles.html")

@app.route("/perfil")
def perfil():
    return render_template("/perfil.html")  






nutrientes = {
    "pollo": {"calorias": 165, "proteina": 31, "carbohidratos": 0, "grasas": 3.6},
    "arroz": {"calorias": 130, "proteina": 2.7, "carbohidratos": 28, "grasas": 0.3},
    "aceite": {"calorias": 884, "proteina": 0, "carbohidratos": 0, "grasas": 100}
}

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        ingredientes = request.form["ingredientes"].split(",")
        total = {"calorias":0, "proteina":0, "carbohidratos":0, "grasas":0}
        
        for item in ingredientes:
            partes = item.strip().split()
            cantidad = int(partes[0].replace("g","").replace("cucharada","1"))  
            nombre = partes[1].lower()
            
            if nombre in nutrientes:
                datos = nutrientes[nombre]
                factor = cantidad / 100
                for k in total:
                    total[k] += datos[k] * factor
        
        resultado = total
    
    return render_template("index.html", resultado=resultado)












if __name__ == '__main__':
    app.run(debug=True)