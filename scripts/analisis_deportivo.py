import pandas as pd
import matplotlib.pyplot as plt

# Leer dataset
df = pd.read_csv("datos/partidos.csv")

# Crear diccionario de estadísticas
equipos = {}

# Obtener nombres únicos de equipos
todos_los_equipos = set(df["equipo_local"]).union(set(df["equipo_visitante"]))

# Inicializar estadísticas
for equipo in todos_los_equipos:
    equipos[equipo] = {
        "puntos": 0,
        "ganados": 0,
        "empatados": 0,
        "perdidos": 0,
        "goles_favor": 0,
        "goles_contra": 0
    }

# Procesar partidos
for _, partido in df.iterrows():

    local = partido["equipo_local"]
    visitante = partido["equipo_visitante"]

    goles_local = partido["goles_local"]
    goles_visitante = partido["goles_visitante"]

    # Goles
    equipos[local]["goles_favor"] += goles_local
    equipos[local]["goles_contra"] += goles_visitante

    equipos[visitante]["goles_favor"] += goles_visitante
    equipos[visitante]["goles_contra"] += goles_local

    # Resultado
    if goles_local > goles_visitante:

        equipos[local]["ganados"] += 1
        equipos[local]["puntos"] += 3

        equipos[visitante]["perdidos"] += 1

    elif goles_local < goles_visitante:

        equipos[visitante]["ganados"] += 1
        equipos[visitante]["puntos"] += 3

        equipos[local]["perdidos"] += 1

    else:

        equipos[local]["empatados"] += 1
        equipos[visitante]["empatados"] += 1

        equipos[local]["puntos"] += 1
        equipos[visitante]["puntos"] += 1

# Crear DataFrame final
tabla = pd.DataFrame(equipos).T

# Diferencia de gol
tabla["diferencia_gol"] = (
    tabla["goles_favor"] - tabla["goles_contra"]
)

# Ordenar tabla
tabla = tabla.sort_values(
    by=["puntos", "diferencia_gol"],
    ascending=False
)

# Mostrar tabla
print("\nTABLA DE POSICIONES\n")
print(tabla)

# Promedio de goles
promedio_goles = (
    df["goles_local"].mean() +
    df["goles_visitante"].mean()
)

print(f"\nPromedio de goles por partido: {promedio_goles:.2f}")

# Gráfico
tabla["puntos"].plot(kind="bar")

plt.title("Puntos por equipo")
plt.xlabel("Equipos")
plt.ylabel("Puntos")

# Guardar gráfico
plt.savefig("resultados/grafico_puntos.png")

print("\nGráfico generado en /resultados")