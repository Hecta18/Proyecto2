from Neo4jConnection import Neo4jConnection 
from Functions import *
from neo4j import GraphDatabase

# Cambia estos datos según tu configuración
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = ""  # Usa la que definiste al iniciar Neo4j

# Datos usuario
nombre_usuario = 'Juan'

# Datos restaurante
nombre_restaurante = 'Burger King'
tipo_restaurante = 'Comida rápida'
calificacion_restaurante = 4.5

# queries
create_usuario = """
CREATE (u:Usuario {nombre: """ + nombre_usuario + """})
RETURN u
"""
create_restaurant = """
CREATE (r:Restaurante {nombre: """ + nombre_restaurante + """, tipo: """ + tipo_restaurante + """, calificacion: """ + calificacion_restaurante + """})
RETURN r
"""
create_relation = """
MATCH (r:Restaurante {nombre: """ + nombre_restaurante + """}), (u:Usuario {nombre: """ + nombre_usuario + """})
CREATE (u)-[:PEDIR]->(r)
RETURN a, b
"""
explicit_feedback = """
MATCH (u:Usuario {nombre: """ + nombre_usuario + """})-[:PEDIR]->(r:Restaurante)<-[:PEDIR]-(otro:Usuario)-[:PIDIÓ]->(sugerido:Restaurante)
WHERE NOT (u)-[:PEDIR]->(sugerido)
RETURN sugerido.nombre
LIMIT 5
"""
content_based = """
MATCH (r:Restaurante)
WHERE r.tipo CONTAINS 'Comida rápida'
  AND r.calificacion >= 4.0
RETURN r.nombre
LIMIT 10
"""

# Crear conexión
conn = Neo4jConnection(URI, USER, PASSWORD)

# Ejecutar consultas
print(queryWithResults(conn, create_usuario))
print(queryWithResults(conn, create_restaurant))
print(queryWithResults(conn, create_relation))

# Cerrar conexión
conn.close()