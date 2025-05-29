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
    if request.method == "POST":
        # lógica para registrar al usuario
        pass
    return render_template("crear_cuenta.html")
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


if __name__ == "__main__":
    app.run(debug=True)
