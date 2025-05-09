#modulo de funciones

#ejecutar y mostrar consulta
def queryWithResults(conn, query):
    # Ejecutar consulta
    resultados = conn.run_query(query)
    # Mostrar resultados
    for r in resultados:
        return r["r"]