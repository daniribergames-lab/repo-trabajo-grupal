import libsql
import envyte
print("Bienvenido al trabajo de Jonathan , Anouar y Daniel")
# Obtenemos las claves de la base de datos tusro desde .env
url = envyte.get("DATABASE_URL")
auth_token = envyte.get("API_TOKEN")

# Nos conectamos a turso
conn = libsql.connect("veterinariodb", sync_url=url, auth_token=auth_token)
conn.sync()
cursor = conn.cursor()

# Menu para mostrar las diferentes operaciones
def mostrar_menu():
    print("\n=== MENU VETERINARIA ===")
    print("1. Ver mascotas")
    print("2. Añadir mascota")
    print("3. Actualizar mascota")
    print("4. Eliminar mascota")
    print("5. Buscar mascotas")
    print("6. Búsquedas avanzadas")
    print("0. Salir")

# Metodo para listar todas las mascotas de la base de datos
def listar_mascotas():
    try:
        cursor.execute("SELECT * FROM Mascota")
        mascotas = cursor.fetchall()
        if not mascotas:
            print("No hay mascotas registradas.")
        else:
            for m in mascotas:
                print(f"ID: {m[0]} | Nombre: {m[1]} | Especie: {m[2]} | Raza: {m[3]} | Sexo: {m[4]} | Edad: {m[6]} años | Médico ID: {m[7]}")
    except Exception as e:
        print(f"Error al obtener la lista de mascotas: {e}")

# Metodo para añadir una nueva mascota
def agregar_mascota():
    try:
        nombre = input("Nombre: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        sexo = input("Sexo (M/F): ")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
        edad = int(input("Edad: "))
        medico_id = int(input("ID del médico veterinario: "))

        cursor.execute("""
            INSERT INTO Mascota (nombre, especie, raza, sexo, fecha_nacimiento, edad, medico_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, especie, raza, sexo, fecha_nacimiento, edad, medico_id))
        conn.commit()
        print(f"Mascota '{nombre}' añadida correctamente.")
    except ValueError:
        print("Error: Edad o ID del médico inválidos. Deben ser números.")
    except Exception as e:
        print(f"No se pudo añadir la mascota: {e}")

# Metodo para actualizar los datos de una mascota
def actualizar_mascota():
    try:
        id_mascota = int(input("ID de la mascota a actualizar: "))
        nuevo_nombre = input("Nuevo nombre: ")
        nueva_raza = input("Nueva raza: ")
        nueva_edad = int(input("Nueva edad: "))

        cursor.execute("""
            UPDATE Mascota SET nombre = ?, raza = ?, edad = ? WHERE id = ?
        """, (nuevo_nombre, nueva_raza, nueva_edad, id_mascota))
        conn.commit()

        # Si se ejecuto la operacion el valor sera 1, sino 0
        if cursor.rowcount == 0:
            print("No se encontró ninguna mascota con ese ID.")
        else:
            print("Mascota actualizada correctamente.")
    except ValueError:
        print("Error: ID y edad deben ser números.")
    except Exception as e:
        print(f"Error al actualizar la mascota: {e}")

# Metodo para eliminar una mascota 
def eliminar_mascota():
    try:
        id_mascota = int(input("ID de la mascota a eliminar: "))
        cursor.execute("DELETE FROM Mascota WHERE id = ?", (id_mascota,))
        conn.commit()

        # Si se ejecuto la operacion el valor sera 1, sino 0
        if cursor.rowcount == 0:
            print("No se encontró una mascota con ese ID.")
        else:
            print("Mascota eliminada correctamente.")
    except ValueError:
        print("Error: el ID debe ser un número.")
    except Exception as e:
        print(f"Error al eliminar la mascota: {e}")

# Metodo para buscar una unica mascota
def buscar_mascota():
    
    try:
        id_mascota = int(input("ID de la mascota a eliminar: "))
        cursor.execute("DELETE FROM Mascota WHERE id = ?", (id_mascota,))
        conn.commit()

        # Si se ejecuto la operacion el valor sera 1, sino 0
        if cursor.rowcount == 0:
            print("No se encontró una mascota con ese ID.")
        else:
            print("Mascota eliminada correctamente.")
    except ValueError:
        print("Error: el ID debe ser un número.")
    except Exception as e:
        print(f"Error al eliminar la mascota: {e}")

# Metodo para buscar una unica mascota
def buscar_mascota():
    try:
        while True:
            print("\n=== BUSCAR MASCOTA ===")
            print("1. Por nombre")
            print("2. Por especie")
            print("3. Por raza")
            print("4. Por edad")
            print("5. Por sexo")
            print("6. Por veterinario asignado")
            print("7. Mostrar todas")
            print("0. Volver al menú principal")

            opcion = input("Elige una opción: ")

            if opcion == "0":
                break
            elif opcion == "1":
                valor = input("Introduce el nombre: ")
                cursor.execute("SELECT * FROM Mascota WHERE nombre LIKE ?", (f"%{valor}%",))
            elif opcion == "2":
                valor = input("Introduce la especie (ej: Perro, Gato): ")
                cursor.execute("SELECT * FROM Mascota WHERE especie LIKE ?", (f"%{valor}%",))
            elif opcion == "3":
                valor = input("Introduce la raza: ")
                cursor.execute("SELECT * FROM Mascota WHERE raza LIKE ?", (f"%{valor}%",))
            elif opcion == "4":
                valor = input("Introduce la edad: ")
                cursor.execute("SELECT * FROM Mascota WHERE edad = ?", (valor,))
            elif opcion == "5":
                valor = input("Introduce el sexo (M/F): ")
                cursor.execute("SELECT * FROM Mascota WHERE sexo = ?", (valor,))
            elif opcion == "6":
                valor = input("Introduce el nombre del veterinario: ")
                cursor.execute("""
                    SELECT M.*
                    FROM Mascota M
                    JOIN Medico_Veterinario V ON M.medico_id = V.id
                    WHERE V.nombre LIKE ?
                """, (f"%{valor}%",))
            elif opcion == "7":
                print("Listado de mascotas :")
                print("------------------------")
                cursor.execute("SELECT * FROM Mascota")
            else:
                print("Opción no válida.")
                continue

            resultados = cursor.fetchall()
            if resultados:
                for m in resultados:
                    print(f"ID: {m[0]} | Nombre: {m[1]} | Especie: {m[2]} | Raza: {m[3]} | Edad: {m[6]} | Médico ID: {m[7]}")
            else:
                print("⚠️ No se encontró ninguna mascota con ese criterio.")

    except Exception as e:
        print(f"Error al buscar mascotas: {e}")


def buscar_avanzado():
    try:
        while True:
            print("\n=== BÚSQUEDAS AVANZADAS ===")
            print("1. Mascotas y su veterinario")
            print("2. Edad media por especie")
            print("3. Número de mascotas por veterinario")
            print("4. Mascotas sin vacunas registradas")
            print("5. Mascotas por rango de edad")
            print("6. Promedio de edad de mascotas por veterinario")
            print("0. Volver al menú principal")

            opcion = input("Elige una opción: ")

            if opcion == "0":
                break

            elif opcion == "1":
                cursor.execute("""
                    SELECT M.nombre, M.especie, M.raza, V.nombre
                    FROM Mascota M
                    JOIN Medico_Veterinario V ON M.medico_id = V.id
                """)
                resultados = cursor.fetchall()
                print("\n🐾 Mascotas y su veterinario:")
                for r in resultados:
                    print(f"Mascota: {r[0]} | Especie: {r[1]} | Raza: {r[2]} | Veterinario: {r[3]}")

            elif opcion == "2":
                cursor.execute("""
                    SELECT especie, ROUND(AVG(edad),2)
                    FROM Mascota
                    GROUP BY especie
                """)
                resultados = cursor.fetchall()
                print("\n Edad media por especie:")
                for r in resultados:
                    print(f"Especie: {r[0]} | Edad media: {r[1]} años")

            elif opcion == "3":
                cursor.execute("""
                    SELECT V.nombre, COUNT(M.id)
                    FROM Medico_Veterinario V
                    LEFT JOIN Mascota M ON M.medico_id = V.id
                    GROUP BY V.nombre
                """)
                resultados = cursor.fetchall()
                print("\n Número de mascotas por veterinario:")
                for r in resultados:
                    print(f"Veterinario: {r[0]} | Mascotas: {r[1]}")

            elif opcion == "4":
                cursor.execute("""
                    SELECT M.nombre, M.especie, M.raza
                    FROM Mascota M
                    LEFT JOIN Vacunas V ON M.id = V.mascota_id
                    WHERE V.id IS NULL
                """)
                resultados = cursor.fetchall()
                print("\n Mascotas sin vacunas registradas:")
                if resultados:
                    for r in resultados:
                        print(f"Mascota: {r[0]} | Especie: {r[1]} | Raza: {r[2]}")
                else:
                    print("Todas las mascotas tienen vacunas registradas.")

            elif opcion == "5":
                # Buscar mascotas por rango de edad
                min_edad = input("Edad mínima: ")
                max_edad = input("Edad máxima: ")
                cursor.execute("""
                    SELECT nombre, especie, raza, edad
                    FROM Mascota
                    WHERE edad BETWEEN ? AND ?
                """, (min_edad, max_edad))
                resultados = cursor.fetchall()
                print(f"\n Mascotas entre {min_edad} y {max_edad} años:")
                if resultados:
                    for r in resultados:
                        print(f"Mascota: {r[0]} | Especie: {r[1]} | Raza: {r[2]} | Edad: {r[3]}")
                else:
                    print("No hay mascotas en ese rango de edad.")

            elif opcion == "6":
                # Promedio de edad de mascotas por veterinario
                cursor.execute("""
                    SELECT V.nombre, ROUND(AVG(M.edad),2)
                    FROM Medico_Veterinario V
                    LEFT JOIN Mascota M ON M.medico_id = V.id
                    GROUP BY V.nombre
                """)
                resultados = cursor.fetchall()
                print("\nPromedio de edad de mascotas por veterinario:")
                for r in resultados:
                    print(f"Veterinario: {r[0]} | Edad media: {r[1]} años")

            else:
                print("Opción no válida.")

    except Exception as e:
        print(f"Error en búsqueda avanzada: {e}")

    
# MENÚ PRINCIPAL
try:
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            listar_mascotas()
        elif opcion == "2":
            agregar_mascota()
        elif opcion == "3":
            actualizar_mascota()
        elif opcion == "4":
            eliminar_mascota()
        elif opcion == "5":
            buscar_mascota()
        elif opcion == "6":
            buscar_avanzado()
        elif opcion == "0":
            print("👋 Saliendo de la agenda...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    try:
        cursor.close()
        conn.close()
        print("Conexión cerrada correctamente.")
    except Exception:
        print("Error al cerrar la conexión.")
