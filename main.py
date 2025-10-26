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
    print("5. Buscar mascota por nombre")
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
        nombre = input("Introduce el nombre a buscar: ")
        cursor.execute("SELECT * FROM Mascota WHERE nombre LIKE ?", (f"%{nombre}%",))
        resultados = cursor.fetchall()
        if resultados:
            for m in resultados:
                print(f"ID: {m[0]} | Nombre: {m[1]} | Especie: {m[2]} | Raza: {m[3]} | Edad: {m[6]}")
        else:
            print("⚠️ No se encontró ninguna mascota con ese nombre.")
    except Exception as e:
        print(f"Error al buscar mascotas: {e}")

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
