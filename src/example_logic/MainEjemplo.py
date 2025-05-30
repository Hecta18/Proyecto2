from Neo4jConnection import Neo4jConnection 
# from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
# import bcrypt

load_dotenv()  
# Cargar variables de entorno desde un archivo .env

# Cambiar datos según configuración
URI = "neo4j+s://33610e87.databases.neo4j.io" #aura
# local => "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.getenv("PASSWORD")
# metodo con archivo .env

# Crear conexión
conn = Neo4jConnection(URI, USER, PASSWORD)

# from Functions import *
from Queries import *
# Ejecutar consultas
try:
    print(queryWithResults(conn, create_usuario, 'u'))
    print(queryWithResults(conn, create_restaurant, 'r'))
    print(queryWithResults(conn, create_perfil, 'p'))
    print(queryWithoutResults(conn, create_relation_order))
    print(queryWithoutResults(conn, create_relation_be))
    # login
    print(login_withCheck(conn, contraseña))
    # print(queryWithResults(conn, explicit_feedback_based))
    # print(queryWithResults(conn, content_based))
    # print(queryWithResults(conn, profile_based))
    # print(hibridRecommendation(explicit_feedback_based, content_based, profile_based, conn))
except Exception as e:
    print(f"Error al ejecutar las consultas: {e}")
# Cerrar conexión
conn.close()