
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route("/recetas")
def recetas():
    return render_template("recetas.html")


if __name__ == '__main__':
    app.run(debug=True)