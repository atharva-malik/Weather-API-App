import requests
from iso3166 import countries
from datetime import datetime
import pytz

#region
api_key = "ede8ff9e889a72caabf0bcec094eb623"
#endregion



def deg_to_compass(degrees):
  """
  Converts degrees (0-360) to cardinal and intercardinal wind directions.

  """

  # Validate input
  if degrees < 0 or degrees > 360:
    raise ValueError("Input degrees must be between 0 and 360")

  # Map degrees to compass directions using a lookup table
  directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
  index = int((degrees / 22.5) + 0.5) % 16
  return directions[index]


def unix_time_to_datetime(unix_time, timezone=None):
  """
  Converts a Unix timestamp to a datetime object in the specified timezone.

  Args:
    unix_time: The Unix timestamp in seconds.
    timezone: An optional timezone object for timezone-aware output.
              If not provided, the local timezone is used.

  Returns:
    A datetime object representing the converted time.
  """

  if timezone:
    return datetime.fromtimestamp(unix_time, tz=timezone)
  else:
    return datetime.fromtimestamp(unix_time)


def get_weather(city: str, more=False) -> int: 
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  # Send GET request and handle response
  response = requests.get(url)
  if 299 >= response.status_code >= 200:
    data = response.json()
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    description = data['weather'][0]['description'].capitalize()

    weather_main = data['weather'][0]['main']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    visibility = data['visibility']
    wind_speed = data['wind']['speed']
    wind_direction = deg_to_compass(data['wind']['deg'])  #TODO: Convert to North East South West
    sunset = unix_time_to_datetime(data['sys']['sunset'], timezone=pytz.timezone("Australia/Sydney"))
    sunsrise = unix_time_to_datetime(data['sys']['sunrise'], timezone=pytz.timezone("Australia/Sydney"))
    if not more:
      print(f"Weather in {city}, {countries.get(country).name}: {temp}°C, {description}")
    print(f"Advanced Weather in {city}, {countries.get(country).name}:")
    print(f"\n\nCurrent Temperature: {temp}°C\nFeels Like: {feels_like}°C\nMax Temperature: {temp_max}°C\nMin Temperature: {temp_min}°C")
    print(f"\n\nWeather condition is {weather_main}, {description}.")
    print(f"\n\nWind speed: {wind_speed} m/s\nWind Direction: {wind_direction}")
    print(f"\n\nSunrise: {sunsrise}\nSunset: {sunset}")
    print(f"\n\nOther weather information:\nPressure: {pressure}\nHumidity: {humidity}\nVisibility: {visibility}")
    return 1
  elif 599 >= response.status_code >= 500:
    print("Error: Server is malfunctioning!")
  elif 499 >= response.status_code >= 400:
    print("Error: User fault! Please check city name and api key!")
  else:
    print("Error: Unknown Error occurred! Please copy the api response and create " \
          "a GitHub bug report.\nError Code: ", response.json)
  return -1
#

def main():
  while True:
    city = input("City Name: ")
    get_weather(city=city, more=True)

if __name__ == "__main__":
  print("Welcome to weather API!")
  main()