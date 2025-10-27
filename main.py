import libsql
import envyte
print("Bienvenido al trabajo de Jonathan , Anouar y Daniel")
# Obtenemos las claves de la base de datos tusro desde .env
url = envyte.get("DATABASE_URL")
auth_token = envyte.get("API_TOKEN")

# Nos conectamos a turso
conn = libsql.connect("veterinaria", sync_url=url, auth_token=auth_token)
conn.sync()
cursor = conn.cursor()

# Menu para mostrar las diferentes operaciones
def mostrar_menu():
    print("\n=== MENU VETERINARIA ===")
    print("1. Listar")
    print("2. Añadir")
    print("3. Actualizar")
    print("4. Eliminar")
    print("5. Buscar")
    print("6. Búsquedas avanzadas")
    print("0. Salir")

# Metodo para listar todas las mascotas de la base de datos
def listar():
    try:
        print("\nSlecciona que deseas gestionar:")
        print("1. Mascotas")
        print("2. Médicos veterinarios")
        print("3. Vacunas")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            cursor.execute("SELECT * FROM Mascota")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("No hay mascotas registradas.")
            else:
                print("\n--- Listado de Mascotas ---")
                for m in mascotas:
                    # Se imprime la lista de mascotas con sus detalles
                    print(f"ID: {m[0]} | Nombre: {m[1]} | Especie: {m[2]} | Raza: {m[3]} | Sexo: {m[4]} | Edad: {m[6]} años | Médico ID: {m[7]}")

        elif opcion == "2":
            cursor.execute("SELECT * FROM Medico_Veterinario")
            medicos = cursor.fetchall()
            if not medicos:
                print("No hay médicos veterinarios registrados.")
            else:
                print("\n--- Listado de Médicos Veterinarios ---")
                for v in medicos:
                    # Se imprime la lista de médicos veterinarios
                    print(f"ID: {v[0]} | Nombre: {v[1]} | Sexo: {v[2]} | Nacimiento: {v[3]} | Edad: {v[4]}")

        elif opcion == "3":
            cursor.execute("""
                SELECT
                    V.id, M.nombre AS mascota_nombre, V.nombre_vacuna, V.fecha_aplicacion, V.proxima_dosis
                FROM Vacunas V
                JOIN Mascota M ON V.mascota_id = M.id
            """)
            vacunas = cursor.fetchall()
            if not vacunas:
                print("No hay vacunas registradas.")
            else:
                print("\n--- Listado de Vacunas ---")
                for v in vacunas:
                    # Se imprime la lista de vacunas con el nombre de la mascota
                    print(f"ID Vacuna: {v[0]} | Mascota: {v[1]} | Vacuna: {v[2]} | Aplicación: {v[3]} | Próxima dosis: {v[4]}")

        else:
            print("Opción no válida.")

    except Exception as e:
        print(f"Error al obtener la lista: {e}")

# Metodo para añadir una nueva mascota
def agregar():
    try:
        print("\n=== AGREGAR REGISTRO ===")
        print("1. Añadir Mascota")
        print("2. Añadir Médico Veterinario")
        print("3. Registrar Vacuna")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            # Añadir mascota
            nombre = input("Nombre de la Mascota: ")
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

        elif opcion == "2":
            # Añadir medico 
            nombre = input("Nombre del Médico: ")
            sexo = input("Sexo (M/F): ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
            edad = int(input("Edad: "))

            cursor.execute("""
                INSERT INTO Medico_Veterinario (nombre, sexo, fecha_nacimiento, edad)
                VALUES (?, ?, ?, ?)
            """, (nombre, sexo, fecha_nacimiento, edad))
            conn.commit()
            print(f"Médico Veterinario '{nombre}' añadido correctamente.")

        elif opcion == "3":
            # Añadir vacuna
            mascota_id = int(input("ID de la mascota: "))
            nombre_vacuna = input("Nombre de la vacuna: ")
            fecha_aplicacion = input("Fecha de aplicación (YYYY-MM-DD): ")
            proxima_dosis = input("Fecha de próxima dosis (YYYY-MM-DD): ")
            observaciones = input("Observaciones (opcional): ")

            cursor.execute("""
                INSERT INTO Vacunas (mascota_id, nombre_vacuna, fecha_aplicacion, proxima_dosis, observaciones)
                VALUES (?, ?, ?, ?, ?)
            """, (mascota_id, nombre_vacuna, fecha_aplicacion, proxima_dosis, observaciones))
            conn.commit()
            print(f"Vacuna '{nombre_vacuna}' registrada para la mascota ID {mascota_id}.")

        else:
            print("Opción no válida.")

    except ValueError:
        print("Error: La edad o los IDs deben ser números enteros.")
    except Exception as e:
        print(f"No se pudo añadir el registro: {e}")

# Metodo para actualizar los datos de una mascota
def actualizar():
    try:
        print("\n=== ACTUALIZAR REGISTRO ===")
        print("1. Actualizar Mascota")
        print("2. Actualizar Médico Veterinario")
        print("3. Actualizar Vacuna")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            # Actualizar mascota
            id_registro = int(input("ID de la mascota a actualizar: "))
            nuevo_nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            nueva_raza = input("Nueva raza (dejar vacío para no cambiar): ")
            nueva_edad = input("Nueva edad (dejar vacío para no cambiar): ")

            updates = []
            params = []

            if nuevo_nombre:
                updates.append("nombre = ?")
                params.append(nuevo_nombre)
            if nueva_raza:
                updates.append("raza = ?")
                params.append(nueva_raza)
            if nueva_edad:
                try:
                    edad_int = int(nueva_edad)
                    updates.append("edad = ?")
                    params.append(edad_int)
                except ValueError:
                    print("La nueva edad debe ser un número y no se actualizará.")

            if not updates:
                print("No se especificaron campos para actualizar.")
                return

            params.append(id_registro)
            sql = f"UPDATE Mascota SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, tuple(params))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró ninguna mascota con ese ID.")
            else:
                print("Mascota actualizada correctamente.")

        elif opcion == "2":
            # Actualizar medico
            id_registro = int(input("ID del médico veterinario a actualizar: "))
            nuevo_nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            nuevo_sexo = input("Nuevo sexo (M/F) (dejar vacío para no cambiar): ")
            nueva_edad = input("Nueva edad (dejar vacío para no cambiar): ")

            updates = []
            params = []

            if nuevo_nombre:
                updates.append("nombre = ?")
                params.append(nuevo_nombre)
            if nuevo_sexo:
                updates.append("sexo = ?")
                params.append(nuevo_sexo)
            if nueva_edad:
                try:
                    edad_int = int(nueva_edad)
                    updates.append("edad = ?")
                    params.append(edad_int)
                except ValueError:
                    print("La nueva edad debe ser un número y no se actualizará.")

            if not updates:
                print("No se especificaron campos para actualizar.")
                return

            params.append(id_registro)
            sql = f"UPDATE Medico_Veterinario SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, tuple(params))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró ningún médico veterinario con ese ID.")
            else:
                print("Médico Veterinario actualizado correctamente.")

        elif opcion == "3":
            # Actualizar vacuna
            id_registro = int(input("ID del registro de vacuna a actualizar: "))
            nueva_dosis = input("Nueva fecha de próxima dosis (YYYY-MM-DD) (dejar vacío para no cambiar): ")
            nuevas_observaciones = input("Nuevas observaciones (dejar vacío para no cambiar): ")

            updates = []
            params = []

            if nueva_dosis:
                updates.append("proxima_dosis = ?")
                params.append(nueva_dosis)
            if nuevas_observaciones:
                updates.append("observaciones = ?")
                params.append(nuevas_observaciones)

            if not updates:
                print("No se especificaron campos para actualizar.")
                return

            params.append(id_registro)
            sql = f"UPDATE Vacunas SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, tuple(params))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró ningún registro de vacuna con ese ID.")
            else:
                print("Registro de vacuna actualizado correctamente.")

        else:
            print("Opción no válida.")

    except ValueError:
        print("Error: El ID del registro debe ser un número entero.")
    except Exception as e:
        print(f"Error al actualizar el registro: {e}")

# Metodo para eliminar una mascota 
def eliminar():
    try:
        print("\n=== ELIMINAR REGISTRO ===")
        print("1. Eliminar Mascota")
        print("2. Eliminar Médico Veterinario")
        print("3. Eliminar Registro de Vacuna")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            # Eliminar mascota
            id_registro = int(input("ID de la mascota a eliminar: "))
            cursor.execute("DELETE FROM Mascota WHERE id = ?", (id_registro,))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró una mascota con ese ID.")
            else:
                print("Mascota eliminada correctamente.")

        elif opcion == "2":
            # Eliminar medico
            id_registro = int(input("ID del médico veterinario a eliminar: "))
            cursor.execute("DELETE FROM Medico_Veterinario WHERE id = ?", (id_registro,))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró un médico veterinario con ese ID.")
            else:
                print("Médico Veterinario eliminado correctamente.")

        elif opcion == "3":
            # Eliminar vacuna
            id_registro = int(input("ID del registro de vacuna a eliminar: "))
            cursor.execute("DELETE FROM Vacunas WHERE id = ?", (id_registro,))
            conn.commit()

            if cursor.rowcount == 0:
                print("No se encontró un registro de vacuna con ese ID.")
            else:
                print("Registro de vacuna eliminado correctamente.")

        else:
            print("Opción no válida.")

    except ValueError:
        print("Error: el ID debe ser un número entero.")
    except Exception as e:
        print(f"Error al eliminar el registro: {e}")

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

# Metodo para buscar mascotas,medicos o vacunas
def buscar():
    try:
        print("\n=== SELECCIONAR TABLA PARA BÚSQUEDA ===")
        print("1. Buscar en Mascotas")
        print("2. Buscar en Médicos Veterinarios")
        print("3. Buscar en Vacunas")
        print("0. Volver al menú principal")

        opcion_tabla = input("Elige una tabla para buscar: ")

        if opcion_tabla == "0":
            return

        # Buscar mascotas
        if opcion_tabla == "1":
            while True:
                print("\n=== BUSCAR MASCOTA ===")
                print("1. Por nombre")
                print("2. Por especie")
                print("3. Por raza")
                print("4. Por edad")
                print("5. Por sexo")
                print("6. Por veterinario asignado")
                print("7. Mostrar todas")
                print("0. Volver al menú de tablas")

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
                        SELECT M.*, V.nombre AS nombre_veterinario
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
                        # La columna 7 es el medico_id
                        print(f"ID: {m[0]} | Nombre: {m[1]} | Especie: {m[2]} | Raza: {m[3]} | Edad: {m[6]} | Médico ID: {m[7]}")
                else:
                    print("No se encontró ninguna mascota con ese criterio.")

        # Buscar medico
        elif opcion_tabla == "2":
            print("\n=== BUSCAR MÉDICO VETERINARIO ===")
            print("1. Por nombre")
            print("2. Por ID")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                valor = input("Introduce el nombre del médico: ")
                cursor.execute("SELECT * FROM Medico_Veterinario WHERE nombre LIKE ?", (f"%{valor}%",))
            elif opcion == "2":
                valor = input("Introduce el ID del médico: ")
                cursor.execute("SELECT * FROM Medico_Veterinario WHERE id = ?", (valor,))
            else:
                print("Opción no válida.")
                return

            resultados = cursor.fetchall()
            if resultados:
                print("\n--- Resultados de Médicos Veterinarios ---")
                for v in resultados:
                    print(f"ID: {v[0]} | Nombre: {v[1]} | Sexo: {v[2]} | Edad: {v[4]} años")
            else:
                print("No se encontró ningún médico con ese criterio.")

        # Buscar vacuna
        elif opcion_tabla == "3":
            print("\n=== BUSCAR REGISTRO DE VACUNA ===")
            print("1. Por nombre de vacuna")
            print("2. Por ID de Mascota")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                valor = input("Introduce el nombre de la vacuna: ")
                cursor.execute("""
                    SELECT V.*, M.nombre AS mascota_nombre
                    FROM Vacunas V
                    JOIN Mascota M ON V.mascota_id = M.id
                    WHERE V.nombre_vacuna LIKE ?
                """, (f"%{valor}%",))
            elif opcion == "2":
                valor = input("Introduce el ID de la mascota: ")
                cursor.execute("""
                    SELECT V.*, M.nombre AS mascota_nombre
                    FROM Vacunas V
                    JOIN Mascota M ON V.mascota_id = M.id
                    WHERE V.mascota_id = ?
                """, (valor,))
            else:
                print("Opción no válida.")
                return

            resultados = cursor.fetchall()
            if resultados:
                print("\n--- Resultados de Vacunas ---")
                for v in resultados:
                    # v[0] es el ID de la vacuna, v[1] es el mascota_id, v[6] es el nombre_mascota
                    print(f"ID Vacuna: {v[0]} | Mascota: {v[6]} (ID: {v[1]}) | Vacuna: {v[2]} | Aplicación: {v[3]} | Próx. Dosis: {v[4]}")
            else:
                print("No se encontró ningún registro de vacuna con ese criterio.")


        else:
            print("Opción de tabla no válida.")

    except ValueError:
        print("Error: El ID o la edad deben ser números.")
    except Exception as e:
        print(f"Error al buscar registros: {e}")


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
                print("\nMascotas y su veterinario:")
                for r in resultados:
                    print(f"Mascota: {r[0]} | Especie: {r[1]} | Raza: {r[2]} | Veterinario: {r[3]}")

            elif opcion == "2":
                cursor.execute("""
                    SELECT especie, ROUND(AVG(edad),2)
                    FROM Mascota
                    GROUP BY especie
                """)
                resultados = cursor.fetchall()
                print("\nEdad media por especie:")
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
                print("\nNúmero de mascotas por veterinario:")
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
                print("\nMascotas sin vacunas registradas:")
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
                print(f"\nMascotas entre {min_edad} y {max_edad} años:")
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
            listar()
        elif opcion == "2":
            agregar()
        elif opcion == "3":
            actualizar()
        elif opcion == "4":
            eliminar()
        elif opcion == "5":
            buscar()
        elif opcion == "6":
            buscar_avanzado()
        elif opcion == "0":
            print("Saliendo de la agenda...")
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