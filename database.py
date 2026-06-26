import sqlite3

DB_NAME = "weather.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

        temperature REAL,

        humidity REAL,

        pressure REAL,

        wind_speed REAL,

        rainfall REAL

    )
    """)

    conn.commit()

    conn.close()


def insert_weather(
    temp,
    humidity,
    pressure,
    wind_speed,
    rainfall
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO weather_data(

        temperature,

        humidity,

        pressure,

        wind_speed,

        rainfall

    )

    VALUES(?,?,?,?,?)

    """, (

        temp,

        humidity,

        pressure,

        wind_speed,

        rainfall

    ))

    conn.commit()

    conn.close()


def get_all_weather():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM weather_data

    ORDER BY id DESC

    LIMIT 50

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def clear_weather_data():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM weather_data"
    )

    conn.commit()

    conn.close()


create_table()