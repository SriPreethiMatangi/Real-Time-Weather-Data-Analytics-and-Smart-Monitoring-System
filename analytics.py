import sqlite3
import pandas as pd

DB_NAME = "weather.db"


def get_weather_analytics():

    try:

        conn = sqlite3.connect(DB_NAME)

        df = pd.read_sql_query(
            "SELECT * FROM weather_data",
            conn
        )

        conn.close()

        if len(df) == 0:

            return {

                "avg_temp": 0,

                "max_temp": 0,

                "min_temp": 0,

                "avg_humidity": 0,

                "avg_rainfall": 0,

                "max_wind": 0,

                "total_records": 0

            }

        analytics = {

            "avg_temp":
            round(df["temperature"].mean(), 2),

            "max_temp":
            round(df["temperature"].max(), 2),

            "min_temp":
            round(df["temperature"].min(), 2),

            "avg_humidity":
            round(df["humidity"].mean(), 2),

            "avg_rainfall":
            round(df["rainfall"].mean(), 2),

            "max_wind":
            round(df["wind_speed"].max(), 2),

            "total_records":
            len(df)

        }

        return analytics

    except Exception as e:

        print("Analytics Error:", e)

        return {

            "avg_temp": 0,

            "max_temp": 0,

            "min_temp": 0,

            "avg_humidity": 0,

            "avg_rainfall": 0,

            "max_wind": 0,

            "total_records": 0

        }


def get_chart_data():

    try:

        conn = sqlite3.connect(DB_NAME)

        df = pd.read_sql_query(
            "SELECT * FROM weather_data ORDER BY id ASC",
            conn
        )

        conn.close()

        return {

            "temperature":
            df["temperature"].tolist(),

            "humidity":
            df["humidity"].tolist(),

            "rainfall":
            df["rainfall"].tolist(),

            "wind_speed":
            df["wind_speed"].tolist()

        }

    except:

        return {

            "temperature": [],

            "humidity": [],

            "rainfall": [],

            "wind_speed": []

        }