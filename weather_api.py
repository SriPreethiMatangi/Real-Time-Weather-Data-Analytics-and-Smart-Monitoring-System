import os
from dotenv import load_dotenv
import requests
load_dotenv()
# Replace with your OpenWeatherMap API Key
API_KEY = os.getenv("API_KEY")
# =========================
# Current Weather
# =========================

def get_weather_data(city="Hyderabad"):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:

        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return None

        rainfall = 0

        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return {

            "city": city,

            "temperature": data["main"]["temp"],

            "humidity": data["main"]["humidity"],

            "pressure": data["main"]["pressure"],

            "wind_speed": data["wind"]["speed"],

            "rainfall": rainfall,

            "description": data["weather"][0]["description"],

            "icon": data["weather"][0]["icon"],

            "lat": data["coord"]["lat"],

            "lon": data["coord"]["lon"]

        }

    except Exception as e:

        print("Weather Error:", e)

        return None


# =========================
# Forecast
# =========================

def get_forecast(city="Hyderabad"):

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:

        response = requests.get(url)
        data = response.json()

        forecast = []

        for item in data["list"][::8]:

            forecast.append({

                "date": item["dt_txt"].split(" ")[0],

                "temp": item["main"]["temp"],

                "humidity": item["main"]["humidity"],

                "icon": item["weather"][0]["icon"],

                "description": item["weather"][0]["description"]

            })

        return forecast[:7]

    except Exception as e:

        print("Forecast Error:", e)

        return []


# =========================
# AQI
# =========================

def get_aqi(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    try:

        response = requests.get(url)
        data = response.json()

        return data["list"][0]["main"]["aqi"]

    except Exception as e:

        print("AQI Error:", e)

        return "N/A"


# =========================
# Global Weather Monitor
# =========================

def get_global_weather():

    cities = [

        "Hyderabad",
        "Delhi",
        "Mumbai",
        "London",
        "New York",
        "Paris",
        "Tokyo",
        "Sydney",
        "Dubai",
        "Singapore",
        "Toronto",
        "Beijing",
        "Moscow",
        "Cape Town",
        "Rio de Janeiro"

    ]

    weather_list = []

    for city in cities:

        weather = get_weather_data(city)

        if weather:

            weather_list.append({

                "city": weather["city"],

                "temperature": weather["temperature"],

                "humidity": weather["humidity"],

                "pressure": weather["pressure"],

                "icon": weather["icon"]

            })

    return weather_list


# =========================
# Testing
# =========================

if __name__ == "__main__":

    print("\nCurrent Weather:\n")
    print(get_weather_data("Hyderabad"))

    print("\nForecast:\n")
    print(get_forecast("Hyderabad"))

    print("\nGlobal Weather:\n")
    print(get_global_weather())