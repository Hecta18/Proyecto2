from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("cuenta.html")

@app.route("/restaurante")
def restaurante():
    return render_template("restaurante.html")

@app.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        correo = request.form["correo"]
        nombre = request.form["nombre"]
        password = request.form["password"]
        confirmar = request.form["confirmar"]

        if password != confirmar:
            return render_template("crear_cuenta.html", error="Las contraseñas no coinciden")

        return redirect(url_for("preguntas"))
    return render_template("crear_cuenta.html")

@app.route("/preguntas", methods=["GET", "POST"])
def preguntas():
    if request.method == "POST":
        comida = request.form["comida"]
        restaurante = request.form["restaurante"]
        precio = request.form["precio"]
        return redirect(url_for("home"))
    return render_template("preguntas.html")

@app.route("/pedido")
def pedido():
    return render_template("pedido.html")


if __name__ == "__main__":
    app.run(debug=True)