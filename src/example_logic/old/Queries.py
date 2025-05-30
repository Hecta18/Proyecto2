from Functions import *

# Datos usuario
nombre_usuario = 'Pedro'
correo = 'email@email.com'
contraseña = '123456' # Implementar seguridad
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
from Functions import hash_password
create_usuario = """
CREATE (u:Usuario {nombre: '""" + nombre_usuario + """', comida: '""" + comida_preferida + """', restaurante: '""" + restaurante_preferido + """', correo: '""" + correo + """', contraseña: '""" + str(hash_password(contraseña)) + """'})
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
login = """
MATCH (u:Usuario {correo: '""" + correo + """'})
RETURN u
"""
hashed_password = """
MATCH (u:Usuario {nombre: '""" + nombre_usuario + """'})
RETURN u.contraseña
"""
search_restaurant = """
MATCH (r:Restaurante {nombre: '""" + nombre_restaurante + """'})
RETURN r
"""
search_restaurant_type = """
MATCH (r:Restaurante {tipo: '""" + tipo_restaurante + """'})
RETURN r
LIMIT 5
"""
# queries recomendación
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

# Funciones de queries
#login con chequeo de contraseña
def login_withCheck(conn, contraseña, query=hashed_password):
    hashed = queryWithResults(conn, query, 'u')
    if check_password(hashed, contraseña):
        print(queryWithoutResults(conn, login, 'u'))