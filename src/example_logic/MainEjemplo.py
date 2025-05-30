from Neo4jConnection import Neo4jConnection 
import os
from dotenv import load_dotenv

load_dotenv()
# Cargar variables de entorno desde un archivo .env

# Cambiar datos según configuración
URI = "neo4j+s://33610e87.databases.neo4j.io" #aura
# local => "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.getenv("PASSWORD")
# metodo con archivo .env

# Crear conexión
try:
    conn = Neo4jConnection(URI, USER, PASSWORD)
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)

# Importar funciones y consultas
from Queries import (
    create_usuario,
    create_restaurant,
    create_perfil,
    create_relation_order,
    create_relation_be,
    login_withCheck,
    queryWithResults,
    queryWithoutResults,
    explicit_feedback_based,
    content_based,
    profile_based,
    hibridRecommendation
)

# Define 'contraseña' variable with a test value or fetch from input/env
contraseña = os.getenv("CONTRASENA", "test_password")

# Ejecutar consultas
try:
    print(queryWithResults(conn, create_usuario, 'u'))
    print(queryWithResults(conn, create_restaurant, 'r'))
    print(queryWithResults(conn, create_perfil, 'p'))
    print(queryWithoutResults(conn, create_relation_order))
    print(queryWithoutResults(conn, create_relation_be))
    # login
    print(login_withCheck(conn, contraseña))
    print(queryWithResults(conn, explicit_feedback_based))
    print(queryWithResults(conn, content_based))
    print(queryWithResults(conn, profile_based))
    print(hibridRecommendation(explicit_feedback_based, content_based, profile_based, conn))
except Exception as e:
    print(f"Error al ejecutar las consultas: {e}")
# Cerrar conexión
conn.close()