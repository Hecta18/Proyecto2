from Neo4jConnection import Neo4jConnection
from Functions import *
import os
from dotenv import load_dotenv

load_dotenv()
# Cargar variables de entorno desde un archivo .env

# Configuración de conexión
URI = "neo4j+s://33610e87.databases.neo4j.io"
USER = "neo4j"
PASSWORD = os.getenv("PASSWORD")
if PASSWORD is None:
    print("Error: PASSWORD environment variable is not set.")
conn = Neo4jConnection(URI, USER, PASSWORD)

def crear_usuario():
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    password = input("Contraseña: ")
    comida = input("Comida preferida: ")
    restaurante = input("Restaurante preferido: ")
    perfil = input("Profesión: ")

    hashed = hash_password(password)

    query = f"""
    CREATE (u:Usuarios {{
        nombre: '{nombre}',
        comida: '{comida}',
        restaurante: '{restaurante}',
        correo: '{correo}',
        contraseña: '{hashed}',
        perfil: '{perfil}'
    }})
    RETURN u
    """
    query2 = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})
    MATCH (p:Perfiles {{nombre: '{perfil}'}})
    CREATE (u)-[:ES]->(p)
    RETURN u
    """
    queryWithoutResults(conn, query)
    queryWithoutResults(conn, query2)
    print("Usuario creado exitosamente.")
    return nombre

def iniciar_sesion():
    correo = input("Correo: ")
    password = input("Contraseña: ")

    query = f"MATCH (u:Usuarios {{correo: '{correo}'}}) RETURN u.nombre AS nombre, u.contraseña AS pass"	
    resultados = conn.run_query(query)

    if not resultados:
        print("Usuario no encontrado.")
        return None

    stored_hash = resultados[0]["pass"]
    nombre = resultados[0]["nombre"]

    if check_password(stored_hash, password):
        print("Inicio de sesión exitoso.")
        return nombre
    else:
        print("Contraseña incorrecta.")
        return None

def hacer_pedido(nombre):
    restaurante = input("Nombre del restaurante al que quieres pedir: ")
    query = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})
    MATCH (r:Restaurantes {{nombre: '{restaurante}'}})
    CREATE (u)-[k:PEDIR]->(r)
    RETURN u, k, r
    """
    queryWithoutResults(conn, query)
    print(f"Pedido realizado a {restaurante}.")

def alterar_datos(nombre):
    nuevo_restaurante = input("Nuevo restaurante favorito: ")
    nueva_comida = input("Nueva comida preferida: ")
    query = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})
    SET u.restaurante = '{nuevo_restaurante}', u.comida = '{nueva_comida}'
    RETURN u
    """
    queryWithoutResults(conn, query)
    print("Datos actualizados correctamente.")

def ver_recomendaciones(nombre):
    explicit = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})-[:PEDIR]->(r:Restaurantes)<-[:PEDIR]-(otro:Usuarios)-[:PEDIR]->(sugerido:Restaurantes)
    WHERE NOT (u)-[:PEDIR]->(sugerido)
    RETURN sugerido.nombre
    LIMIT 5
    """
    content = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})
    MATCH (r:Restaurantes)
    WHERE r.tipo CONTAINS u.comida OR r.nombre CONTAINS u.restaurante
    RETURN r.nombre
    LIMIT 5
    """
    profile = f"""
    MATCH (u:Usuarios {{nombre: '{nombre}'}})-[:ES]->(p:Perfiles)
    MATCH (r:Restaurantes)
    WHERE r.calificacion >= p.calificacion
    RETURN r.nombre
    LIMIT 5
    """

    print("Recomendaciones basadas en feedback explícito:")
    print(queryWithResults(conn, explicit, 'sugerido.nombre'))

    print("Recomendaciones basadas en contenido:")
    print(queryWithResults(conn, content, 'r.nombre'))

    print("Recomendaciones basadas en perfil:")
    print(queryWithResults(conn, profile, 'r.nombre'))

    print("Recomendación híbrida:")
    hibridas = hibridRecommendation(explicit, content, profile, conn)
    for r in hibridas:
        print(f"- {r['r.nombre']}")

def menu_usuario(nombre):
    while True:
        print(f"\nBienvenido, {nombre}. ¿Qué deseas hacer?")
        print("1. Hacer un pedido")
        print("2. Alterar mis datos")
        print("3. Ver recomendaciones")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            hacer_pedido(nombre)
        elif opcion == "2":
            alterar_datos(nombre)
        elif opcion == "3":
            ver_recomendaciones(nombre)
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

def main():
    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Crear usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            try:
                nombre = crear_usuario()
                menu_usuario(nombre)
            except Exception as e:
                print(f"Error al crear usuario: {e}")
        elif opcion == "2":
            try:
                nombre = iniciar_sesion()
                if nombre:
                    menu_usuario(nombre)
            except Exception as e:
                print(f"Error al iniciar sesión: {e}")
        elif opcion == "3":
            print("Gracias por usar la app.")
            break
        else:
            print("Opción inválida.")

    conn.close()

if __name__ == "__main__":
    main()
