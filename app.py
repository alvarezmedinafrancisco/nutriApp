from flask import Flask,render_template
app = Flask(__name__)

@app.route('/base')
def index():
    return render_template('base.html')

@app.route('/info')
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

@app.route("/registrate")
def registrate():
    return render_template("/registrate.html")

@app.route("/utiles")
def utiles():
    return render_template("/utiles.html")

if __name__ == '__main__':
    app.run(debug=True)