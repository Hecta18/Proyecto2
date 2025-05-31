import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, request, redirect, url_for, session
from Neo4jConnection import Neo4jConnection
from neo4j import GraphDatabase


app = Flask(__name__)
# Conexión a la base de datos Neo4j Aura
conn = Neo4jConnection(
    "neo4j+s://33610e87.databases.neo4j.io",  # URI de Aura
    "neo4j",                                  # Usuario por defecto
    "PASSWORD"              # 👈 Reemplaza esto con tu contraseña real
)

# Prueba de conexión
print("Probando conexión a Neo4j...")
try:
    resultado = conn.run_query("RETURN '¡Conexión exitosa!' AS mensaje")
    print(resultado[0]['mensaje'])  # Imprime: ¡Conexión exitosa!
except Exception as e:
    print("Error al conectar a Neo4j:", e)


app.secret_key = "clave_secreta"
# Configuración de la clave secreta para la sesión
todos_restaurantes = [
    {
        "nombre": "Burger King",
        "imagen": "https://www.pngall.com/wp-content/uploads/13/Burger-King-Logo-PNG-Clipart.png",
        "tipo": "Hamburguesas",
        "platos": [
            {"nombre": "Whopper", "descripcion": "Hamburguesa con carne a la parrilla", "precio": 35},
            {"nombre": "Papas grandes", "descripcion": "Papas fritas crujientes", "precio": 18}
        ]
    },
    {
        "nombre": "Pizza Hut",
        "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/Pizza-Hut-Logo-1999.jpg",
        "tipo": "Pizza",
        "platos": [
            {"nombre": "Pizza Suprema", "descripcion": "Pizza con todo", "precio": 50},
            {"nombre": "Pan de ajo", "descripcion": "Pan con mantequilla y ajo", "precio": 15}
        ]
    },
    {
        "nombre": "Sushi Itto",
        "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEX4IpoSFlx0lmkGB4w5W1IY3XKC81wPW9Mw&s",
        "tipo": "Sushi",
        "platos": [
            {"nombre": "Sushi variado", "descripcion": "Selección de sushi fresco", "precio": 60},
            {"nombre": "Rollos de atún", "descripcion": "Rollos de atún con aguacate", "precio": 45}
        ]
    },
    {
        "nombre": "Domino's",
        "imagen": "https://prestonchamber.org/wp-content/uploads/2024/06/dominos.png",
        "tipo": "Pizza",
        "platos": [
            {"nombre": "Margarita", "descripcion": "Pizza clásica con tomate y queso", "precio": 40},
            {"nombre": "Pepperoni", "descripcion": "Pizza con rodajas de pepperoni", "precio": 45}
        ]
    },
    {
        "nombre": "Subway",
        "imagen": "https://m.media-amazon.com/images/G/01/AdProductsWebsite/images/CaseStudies/Subway_-_Thumbnail.jpg",
        "tipo": "Sandwich",
        "platos": [
            {"nombre": "Sub de pollo", "descripcion": "Sándwich de pollo a la parrilla", "precio": 30},
            {"nombre": "Sub vegetariano", "descripcion": "Sándwich con vegetales frescos", "precio": 25}
        ]
    },
    {
        "nombre": "KFC",
        "imagen": "https://1000marcas.net/wp-content/uploads/2020/01/KFC-logo.png",
        "tipo": "Hamburguesas",
        "platos": [
            {"nombre": "Pollo frito", "descripcion": "Pollo frito crujiente", "precio": 50},
            {"nombre": "Tiras de pollo", "descripcion": "Tiras de pollo empanizadas", "precio": 35}
        ]
    },
    {
        "nombre": "Taco Bell",
        "imagen": "https://cdn.worldvectorlogo.com/logos/taco-bell-7.svg",
        "tipo": "Hamburguesas",
        "platos": [
            {"nombre": "Tacos al pastor", "descripcion": "Tacos con carne al pastor", "precio": 20},
            {"nombre": "Burrito grande", "descripcion": "Burrito relleno de frijoles y carne", "precio": 30}
        ]
    },
    {
        "nombre": "Wendy's",
        "imagen": "https://cdn.worldvectorlogo.com/logos/wendys-1.svg",
        "tipo": "Hamburguesas",
        "platos": [
            {"nombre": 'Hamburguesa clásica', "descripcion": "Hamburguesa con lechuga y tomate", "precio": 28},
            {"nombre": "Papas fritas", "descripcion": "Papas fritas crujientes", "precio": 15}
        ]
    },
    {
        "nombre": "McDonald's",
        "imagen": "https://1000marcas.net/wp-content/uploads/2019/11/McDonalds-logo.png",
        "tipo": "Hamburguesas",
        "platos": [
            {"nombre": "Big Mac", "descripcion": "Hamburguesa con dos carnes y salsa especial", "precio": 40},
            {"nombre": "McFlurry", "descripcion": "Postre helado con trozos de chocolate", "precio": 20}
        ]
    },
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    tipo = request.form.get("tipo_comida")
    buscar = request.form.get("busqueda")

    restaurantes_filtrados = todos_restaurantes

    if tipo and tipo != "Todos":
        restaurantes_filtrados = [r for r in restaurantes_filtrados if r.get("tipo") == tipo]

    if buscar:
        buscar_lower = buscar.lower()
        restaurantes_filtrados = [r for r in restaurantes_filtrados if buscar_lower in r["nombre"].lower()]

    return render_template("home.html", restaurantes=restaurantes_filtrados, tipo_seleccionado=tipo or "Todos", texto_busqueda=buscar or "")

@app.route("/restaurante/<nombre>")
def restaurante(nombre):
    restaurante = next((r for r in todos_restaurantes if r["nombre"] == nombre), None)
    if not restaurante:
        return "Restaurante no encontrado", 404
    return render_template("restaurante.html", restaurante=restaurante)

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
            return redirect(url_for("home"))

    return render_template("crear_cuenta.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("cuenta.html")

if __name__ == "__main__":
    app.run(debug=True)