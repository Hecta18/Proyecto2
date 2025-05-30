from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    restaurantes = [
        {"nombre": "Burger King", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Burger-King-Logo.png"},
        {"nombre": "Pizza Hut", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Pizza-Hut-Logo.png"},
        {"nombre": "Sushi Itto", "imagen": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Sushi_Itto_logo.png"},
        {"nombre": "Domino's", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Dominos-Logo.png"},
        {"nombre": "Subway", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Subway-Logo.png"},
        {"nombre": "KFC", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/KFC-Logo.png"},
        {"nombre": "Taco Bell", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Taco-Bell-Logo.png"},
        {"nombre": "Wendy's", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Wendys-Logo.png"},
        {"nombre": "Popeyes", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Popeyes-Logo.png"}
    ]
    return render_template("home.html", restaurantes=restaurantes)


@app.route("/agregar_pedido", methods=["POST"])
def agregar_pedido():
    plato = request.form["plato"]
    precio = float(request.form["precio"])

    if "carrito" not in session:
        session["carrito"] = []

    session["carrito"].append({"plato": plato, "precio": precio})
    session.modified = True

    return redirect(url_for("pedido"))

@app.route("/pedido")
def pedido():
    carrito = session.get("carrito", [])
    total = sum(item["precio"] for item in carrito)
    return render_template("pedido.html", carrito=carrito, total=total)

@app.route("/eliminar_pedido/<int:index>", methods=["POST"])
def eliminar_pedido(index):
    if "carrito" in session and 0 <= index < len(session["carrito"]):
        del session["carrito"][index]
        session.modified = True
    return redirect(url_for("pedido"))

@app.route("/crear_cuenta", methods=["GET", "POST"])
def crear_cuenta():
    error = ""
    if request.method == "POST":
        correo = request.form["correo"]
        nombre = request.form["nombre"]
        password = request.form["password"]
        confirmar = request.form["confirmar"]

        if password != confirmar:
            error = "La contraseña no coincide"
        else:
            return redirect(url_for("cuenta"))

    return render_template("crear_cuenta.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    restaurantes = [
        {
            "nombre": "Burger King",
            "imagen": "https://i.ytimg.com/vi/dl2cuK5eahM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLByczZK5avV920IHrsKmKUyk_Ut3A"
        },
        {
            "nombre": "Pizza Hut",
            "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Pizza-Hut-Logo-1999.jpg"
        },
        {
            "nombre": "Sushi Itto",
            "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEX4IpoSFlx0lmkGB4w5W1IY3XKC81wPW9Mw&s"
        },
        {
            "nombre": "Little Caesars",
            "imagen": "https://centranorte.com.gt/wp-content/uploads/2023/06/little-caesars.jpg"
        },
        
        
    ]
    return render_template("home.html", restaurantes=restaurantes)


@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("cuenta.html")


if __name__ == "__main__":
    app.run(debug=True)
