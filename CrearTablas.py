import sqlite3

with sqlite3.connect("veterinaria.db") as conn:
    cursor = conn.cursor()

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS Medico_Veterinario (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                sexo TEXT NOT NULL,
                fecha_nacimiento DATE,
                edad INTEGER
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
