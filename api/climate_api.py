"""
Terra 2.0 — Climate API Module
Integrates with Open-Meteo for weather, AQI, and geocoding.
All endpoints are free and require no API key.
"""

from datetime import datetime

import requests

from config import DEFAULT_LAT, DEFAULT_LON, DEFAULT_CITY


class ClimateAPI:
    """Fetches weather, AQI, and location data from Open-Meteo."""

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_coordinates(city: str) -> dict:
        """
        Get lat/lon coordinates for a city name.
        Returns {"lat": float, "lon": float, "city": str}
        Defaults to Chennai on error.
        """
        try:
            response = requests.get(
                ClimateAPI.GEOCODING_URL,
                params={"name": city, "count": 1, "language": "en"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return {
                    "lat": result.get("latitude", DEFAULT_LAT),
                    "lon": result.get("longitude", DEFAULT_LON),
                    "city": result.get("name", city),
                }
        except (requests.RequestException, KeyError, IndexError, ValueError):
            pass

        return {
            "lat": DEFAULT_LAT,
            "lon": DEFAULT_LON,
            "city": DEFAULT_CITY,
        }

    @staticmethod
    def get_aqi(lat: float, lon: float) -> dict:
        """
        Get Air Quality Index data.
        Returns {"pm2_5": float, "pm10": float, "aqi": int,
                 "category": str, "color": str, "emoji": str}
        """
        try:
            response = requests.get(
                ClimateAPI.AQI_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "pm2_5,pm10,european_aqi",
                    "forecast_days": 1,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            hourly = data.get("hourly", {})
            current_hour = datetime.now().hour

            pm2_5_values = hourly.get("pm2_5", [])
            pm10_values = hourly.get("pm10", [])
            aqi_values = hourly.get("european_aqi", [])

            # Get current hour's values (with bounds checking)
            idx = min(current_hour, len(pm2_5_values) - 1) if pm2_5_values else 0

            pm2_5 = pm2_5_values[idx] if idx < len(pm2_5_values) else 0
            pm10 = pm10_values[idx] if idx < len(pm10_values) else 0
            aqi = aqi_values[idx] if idx < len(aqi_values) else 0

            # Handle None values
            pm2_5 = pm2_5 if pm2_5 is not None else 0
            pm10 = pm10 if pm10 is not None else 0
            aqi = aqi if aqi is not None else 0

            # Categorize
            if aqi <= 20:
                category, color, emoji = "Good", "#22C55E", "😊"
            elif aqi <= 40:
                category, color, emoji = "Fair", "#84CC16", "🙂"
            elif aqi <= 80:
                category, color, emoji = "Moderate", "#F59E0B", "😐"
            elif aqi <= 160:
                category, color, emoji = "Poor", "#EF4444", "😷"
            else:
                category, color, emoji = "Very Poor", "#7C3AED", "🤢"

            return {
                "pm2_5": round(pm2_5, 1),
                "pm10": round(pm10, 1),
                "aqi": int(aqi),
                "category": category,
                "color": color,
                "emoji": emoji,
            }

        except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
            return {
                "pm2_5": 0,
                "pm10": 0,
                "aqi": 0,
                "category": "Unknown",
                "color": "#6B7280",
                "emoji": "❓",
            }

    @staticmethod
    def get_weather(lat: float, lon: float) -> dict:
        """
        Get current weather data.
        Returns {"temperature": float, "humidity": float,
                 "weather_code": int, "wind_speed": float,
                 "description": str, "emoji": str}
        """
        try:
            response = requests.get(
                ClimateAPI.WEATHER_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                    "timezone": "Asia/Kolkata",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            temp = current.get("temperature_2m", 0)
            humidity = current.get("relative_humidity_2m", 0)
            weather_code = current.get("weather_code", 0)
            wind_speed = current.get("wind_speed_10m", 0)

            # Weather code to description and emoji
            weather_map = {
                0: ("Clear sky", "☀️"),
                1: ("Mainly clear", "🌤️"),
                2: ("Partly cloudy", "⛅"),
                3: ("Overcast", "☁️"),
                45: ("Foggy", "🌫️"),
                48: ("Rime fog", "🌫️"),
                51: ("Light drizzle", "🌦️"),
                53: ("Moderate drizzle", "🌦️"),
                55: ("Dense drizzle", "🌧️"),
                61: ("Slight rain", "🌧️"),
                63: ("Moderate rain", "🌧️"),
                65: ("Heavy rain", "⛈️"),
                71: ("Slight snow", "🌨️"),
                73: ("Moderate snow", "🌨️"),
                75: ("Heavy snow", "❄️"),
                77: ("Snow grains", "❄️"),
                80: ("Slight showers", "🌦️"),
                81: ("Moderate showers", "🌧️"),
                82: ("Violent showers", "⛈️"),
                85: ("Slight snow showers", "🌨️"),
                86: ("Heavy snow showers", "❄️"),
                95: ("Thunderstorm", "⛈️"),
                96: ("Thunderstorm + hail", "⛈️"),
                99: ("Thunderstorm + heavy hail", "⛈️"),
            }

            description, emoji = weather_map.get(
                weather_code, ("Unknown", "🌡️")
            )

            return {
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1),
                "weather_code": weather_code,
                "wind_speed": round(wind_speed, 1),
                "description": description,
                "emoji": emoji,
            }

        except (requests.RequestException, KeyError, ValueError, TypeError):
            return {
                "temperature": 0,
                "humidity": 0,
                "weather_code": 0,
                "wind_speed": 0,
                "description": "Unavailable",
                "emoji": "❓",
            }
