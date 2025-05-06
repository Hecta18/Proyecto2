from Neo4jConnection import Neo4jConnection 
from neo4j import GraphDatabase

# Cambia estos datos según tu configuración
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = ""  # Usa la que definiste al iniciar Neo4j

# Crear un nodo de prueba
create_query = """
CREATE (r:Restaurante {nombre: 'Taco Loco', tipo: 'Mexicana'})
RETURN r
"""
query = """
MATCH (r:Restaurante)
WHERE r.tipo = 'Mexicana'
RETURN r.nombre AS nombre
"""

# Crear conexión
conn = Neo4jConnection(URI, USER, PASSWORD)

# Ejecutar consulta
resultados = conn.run_query(create_query)

# Mostrar resultados
for r in resultados:
    print(r["r"])

resultados = conn.run_query(query)

for r in resultados:
    print(r["nombre"])

# Cerrar conexión
conn.close()