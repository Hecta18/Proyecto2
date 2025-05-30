from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/restaurante")
def restaurante():
    return render_template("restaurante.html")

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

@app.route("/home", methods=["GET", "POST"])
def home():
    todos_restaurantes = [
        {"nombre": "Burger King", "imagen": "https://www.pngall.com/wp-content/uploads/13/Burger-King-Logo-PNG-Clipart.png"},
        {"nombre": "Pizza Hut", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Pizza-Hut-Logo-1999.jpg"},
        {"nombre": "Sushi Itto", "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEX4IpoSFlx0lmkGB4w5W1IY3XKC81wPW9Mw&s"},
        {"nombre": "Domino's", "imagen": "https://prestonchamber.org/wp-content/uploads/2024/06/dominos.png"},
        {"nombre": "Subway", "imagen": "https://m.media-amazon.com/images/G/01/AdProductsWebsite/images/CaseStudies/Subway_-_Thumbnail.jpg"},
        {"nombre": "KFC", "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/KFC-logo.png"},
        {"nombre": "Taco Bell", "imagen": "https://cdn.worldvectorlogo.com/logos/taco-bell-7.svg"},
        {"nombre": "Wendy's", "imagen": "https://cdn.worldvectorlogo.com/logos/wendys-1.svg"},
        {"nombre": "McDonald's", "imagen": "https://1000marcas.net/wp-content/uploads/2019/11/McDonalds-logo.png"}
    ]
    tipo = request.form.get("tipo_comida")

    if tipo and tipo != "Todos":
        restaurantes = [r for r in todos_restaurantes if r["tipo"] == tipo]
    else:
        restaurantes = todos_restaurantes

    return render_template("home.html", restaurantes=restaurantes, tipo_seleccionado=tipo)
@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("cuenta.html")


if __name__ == "__main__":
    app.run(debug=True)
