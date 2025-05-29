#modulo de funciones
from MainEjemplo import login, hashed_password

#hashear contraseña
def hash_password(password):
    # Genera salt(valor aleatorio) y hashea
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

#verificar contraseña
def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

#login con chequeo de contraseña
def login_withCheck(conn, contraseña, query=hashed_password):
    if check_password(queryWithResults(conn, query, 'u'), contraseña) == True:
            print(queryWithoutResults(conn, login, 'u'))
        
#ejecutar consulta
def queryWithoutResults(conn, query):
    # Ejecutar consulta
    conn.run_query(query)
    
#ejecutar y mostrar consulta
def queryWithResults(conn, query, alias):
    # Ejecutar consulta
    resultados = conn.run_query(query)
    # Mostrar resultados
    for r in resultados:
        return r[alias]
    
#Algoritmo Intersección de conjuntos(set), complejidad O(n)
#Set = unordered collection of unique elements.
def resultados_comunes(lista1, lista2, lista3):
    set1 = set(lista1)
    set2 = set(lista2)
    set3 = set(lista3)

    # Intersección de los tres conjuntos
    comunes = set1 & set2 & set3
    return list(comunes)

#Algoritmo de recomendación híbrido, comunes entre las 3 recomendaciones
def hibridRecommendation(query1, query2, query3, conn):
    # Ejecutar consultas
    resultados1 = conn.run_query(query1)
    resultados2 = conn.run_query(query2)
    resultados3 = conn.run_query(query3)
    # Retornar resultados repetidos
    return resultados_comunes(resultados1, resultados2, resultados3)
    