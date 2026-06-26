from flask import Flask, render_template, request, Response
from weather_api import (
    get_weather_data,
    get_forecast,
    get_aqi,
    get_global_weather
)

from database import (
    insert_weather,
    get_all_weather
)

from analytics import (
    get_weather_analytics,
    get_chart_data
)

import sqlite3
import csv
from io import StringIO

app = Flask(__name__)


@app.route("/")
def dashboard():

    city = request.args.get(
        "city",
        "Hyderabad"
    )

    weather = get_weather_data(city)

    forecast = []

    aqi = "N/A"

    if weather:

        forecast = get_forecast(city)

        aqi = get_aqi(
            weather["lat"],
            weather["lon"]
        )

        insert_weather(
            weather["temperature"],
            weather["humidity"],
            weather["pressure"],
            weather["wind_speed"],
            weather["rainfall"]
        )

    analytics = get_weather_analytics()

    history = get_all_weather()

    chart_data = get_chart_data()

    # Global Weather Monitor
    global_weather = get_global_weather()

    alert = "Normal Weather"

    if weather:

        if weather["temperature"] > 40:

            alert = "🔥 High Temperature Warning"

        elif weather["humidity"] < 20:

            alert = "⚠️ Low Humidity Warning"

        elif weather["wind_speed"] > 15:

            alert = "🌪️ Strong Wind Alert"

    return render_template(

        "index.html",

        city=city,

        weather=weather,

        forecast=forecast,

        aqi=aqi,

        analytics=analytics,

        history=history,

        chart_data=chart_data,

        global_weather=global_weather,

        alert=alert

    )


@app.route("/export")
def export_csv():

    conn = sqlite3.connect("weather.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM weather_data"
    )

    rows = cursor.fetchall()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",
        "Timestamp",
        "Temperature",
        "Humidity",
        "Pressure",
        "Wind Speed",
        "Rainfall"

    ])

    writer.writerows(rows)

    output.seek(0)

    return Response(

        output,

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=weather_data.csv"
        }

    )


@app.route("/about")
def about():

    return """
    <h2>
    Real-Time Weather Data Analytics and Smart Monitoring System
    </h2>

    <p>
    Developed using Flask, SQLite,
    OpenWeatherMap API and Chart.js
    </p>
    """


if __name__ == "__main__":

    app.run(debug=True)