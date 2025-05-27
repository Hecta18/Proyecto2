from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Simulación de usuarios registrados
usuarios = [
    {"email": "diego@example.com", "password": "1234"},
    {"email": "giancarlo@example.com", "password": "abcd"}
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Verificar si el usuario existe
        for user in usuarios:
            if user["email"] == email and user["password"] == password:
                return redirect(url_for("home"))
        flash("Correo o contraseña incorrectos")
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/cuenta', methods=["GET", "POST"])
def cuenta():
    return render_template("cuenta.html")

@app.route('/restaurante')
def restaurante():
    return render_template("restaurante.html")

if __name__ == "__main__":
    app.run(debug=True)