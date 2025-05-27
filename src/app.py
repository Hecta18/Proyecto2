from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Simulación de login exitoso
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        # Procesar cambios de cuenta
        return redirect(url_for("home"))
    return render_template("cuenta.html")

@app.route("/restaurante")
def restaurante():
    return render_template("restaurante.html")

if __name__ == "__main__":
    app.run(debug=True)
