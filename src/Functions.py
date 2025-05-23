#modulo de funciones

#ejecutar y mostrar consulta
def queryWithResults(conn, query):
    # Ejecutar consulta
    resultados = conn.run_query(query)
    # Mostrar resultados
    for r in resultados:
        return r["r"]
    
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
    
