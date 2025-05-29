from Neo4jConnection import Neo4jConnection 
from Functions import *
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()  # Cargar variables de entorno desde un archivo .env

# Cambia estos datos según configuración
URI = "neo4j+s://33610e87.databases.neo4j.io" #aura
# local = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = os.getenv("PASSWORD")
# metodo con archivo .env

# Datos usuario
nombre_usuario = 'Pedro'
comida_preferida = 'Hamburguesas'
restaurante_preferido = 'Burger King'

# Datos restaurante
nombre_restaurante = 'Burger King'
tipo_restaurante = 'Hamburguesas'
calificacion_restaurante = 4.5

# Datos perfil
nombre_perfil = 'Influencer'
calificacion_recomendacion = 4.0

# queries
create_usuario = """
CREATE (u:Usuario {nombre: '""" + nombre_usuario + """', comida: '""" + comida_preferida + """', restaurante: '""" + restaurante_preferido + """'})
RETURN u
"""
create_restaurant = """
CREATE (r:Restaurante {nombre: '""" + nombre_restaurante + """', tipo: '""" + tipo_restaurante + """', calificacion: """ + str(calificacion_restaurante) + """})
RETURN r
"""
create_perfil = """
CREATE (p:Perfil {nombre: '""" + nombre_perfil + """', calificacion: """ + str(calificacion_recomendacion) + """})
RETURN p
"""
create_relation_order = """
MATCH (r:Restaurante {nombre: '""" + nombre_restaurante + """'}), (u:Usuario {nombre: '""" + nombre_usuario + """'})
CREATE (u)-[:PEDIR]->(r)
RETURN u, r
"""
create_relation_be = """
MATCH (p:Perfil {nombre: '""" + nombre_perfil + """'}), (u:Usuario {nombre: '""" + nombre_usuario + """'})
CREATE (u)-[:ES]->(p)
RETURN u, p
"""
explicit_feedback_based = """
MATCH (u:Usuario {nombre: '""" + nombre_usuario + """'})-[:PEDIR]->(r:Restaurante)<-[:PEDIR]-(otro:Usuario)-[:PEDIR]->(sugerido:Restaurante)
WHERE NOT (u)-[:PEDIR]->(sugerido)
RETURN sugerido.nombre
LIMIT 5
"""
content_based = """
MATCH (r:Restaurante)
WHERE r.tipo CONTAINS '""" + tipo_restaurante + """'
  AND r.calificacion >= 4.0
RETURN r.nombre
LIMIT 5
"""
profile_based = """
MATCH (u:Usuario {nombre: '""" + nombre_usuario + """'})-[:ES]->(p:Perfil)
MATCH (r:Restaurante)
WHERE r.calificacion >= p.calificacion
RETURN r.nombre
LIMIT 5
"""

# Crear conexión
conn = Neo4jConnection(URI, USER, PASSWORD)

# Ejecutar consultas
try:
    print(queryWithResults(conn, create_usuario, 'u'))
    print(queryWithResults(conn, create_restaurant, 'r'))
    print(queryWithResults(conn, create_perfil, 'p'))
    print(queryWithoutResults(conn, create_relation_order))
    print(queryWithoutResults(conn, create_relation_be))
    # print(queryWithResults(conn, explicit_feedback_based))
    # print(queryWithResults(conn, content_based))
    # print(queryWithResults(conn, profile_based))
    # print(hibridRecommendation(explicit_feedback_based, content_based, profile_based, conn))
except Exception as e:
    print(f"Error al ejecutar las consultas: {e}")
# Cerrar conexión
conn.close()