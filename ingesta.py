import sqlite3
import libsql
import envyte

try:
    # Obtenemos las claves de la base de datos tusro desde .env
    url = envyte.get("DATABASE_URL")
    auth_token = envyte.get("API_TOKEN")

    # Nos conectamos a turso
    conn = libsql.connect("veterinariodb", sync_url=url, auth_token=auth_token)
    conn.sync()

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Medico_Veterinario")
    cursor.execute("DROP TABLE IF EXISTS Mascota")
    cursor.execute("DROP TABLE IF EXISTS Vacunas")

    # Se crean las tablas
    cursor.execute('''CREATE TABLE IF NOT EXISTS Medico_Veterinario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        sexo TEXT NOT NULL,
        fecha_nacimiento DATE,
        edad INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Mascota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        especie TEXT NOT NULL,
        raza TEXT NOT NULL,
        sexo TEXT NOT NULL,
        fecha_nacimiento DATE,
        edad INTEGER NOT NULL,
        medico_id INTEGER,
        FOREIGN KEY (medico_id) REFERENCES Medico_Veterinario(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Vacunas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mascota_id INTEGER NOT NULL,
        nombre_vacuna TEXT NOT NULL,
        fecha_aplicacion DATE,
        proxima_dosis DATE,
        observaciones TEXT,
        FOREIGN KEY (mascota_id) REFERENCES Mascota(id) ON DELETE CASCADE
    )''')

    conn.commit()
    print("Tablas creadas correctamente y sincronizadas con Turso.")

    # Ingesta de datos iniciales
    veterinarios = [
        ("Laura Gómez", "F", "1985-07-14", 39),
        ("Carlos Pérez", "M", "1990-02-03", 35)
    ]

    for vet in veterinarios:
        cursor.execute(
            "INSERT INTO Medico_Veterinario (nombre, sexo, fecha_nacimiento, edad) VALUES (?, ?, ?, ?)",
            vet
        )

    mascotas = [
        ("Toby", "Perro", "Labrador", "M", "2019-04-20", 6, 1),
        ("Misu", "Gato", "Siames", "F", "2020-06-12", 5, 2)
    ]

    for mascota in mascotas:
        cursor.execute(
            "INSERT INTO Mascota (nombre, especie, raza, sexo, fecha_nacimiento, edad, medico_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            mascota
        )

    vacunas = [
        (1, "Rabia", "2024-03-01", "2025-03-01", "Sin reacciones"),
        (2, "Triple Felina", "2024-02-10", "2025-02-10", "Revisión anual")
    ]

    for vacuna in vacunas:
        cursor.execute(
            "INSERT INTO Vacunas (mascota_id, nombre_vacuna, fecha_aplicacion, proxima_dosis, observaciones) VALUES (?, ?, ?, ?, ?)",
            vacuna
        )

    conn.commit()
    print("Ingesta inicial completada con éxito.")

except Exception as e:
    print(f"Error durante la ejecución: {e}")

finally:
    conn.close()
    print("Conexión cerrada correctamente.")
