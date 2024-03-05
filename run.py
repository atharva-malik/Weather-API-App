import requests, keyboard, time, pytz; from iso3166 import countries; from datetime import datetime; from simple_colors import *; from os import system, name

from pprint import pprint

#region
api_key = "ede8ff9e889a72caabf0bcec094eb623"
#endregion


def clear():
  # # for windows
  # if name == 'nt':
  #   _ = system('cls')
  # # for mac and linux(here, os.name is 'posix')
  # else:
  #   _ = system('clear')
  pass


def deg_to_compass(degrees):
  """
  Converts degrees (0-360) to cardinal and intercardinal wind directions.

  """

  # Validate input
  if degrees < 0 or degrees > 360:
    raise ValueError("Input degrees must be between 0 and 360")

  # Map degrees to compass directions using a lookup table
  directions = ["North", "North North East", "North East", "East North East", "East", "East South East", "South East", "South South East",
                "South", "South South West", "South West", "West South West", "West", "West North West", "North West", "North North West"]
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


def get_future_forecast(city: str, days: int, more=False) -> int:
  url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
  response = requests.get(url)
  if 299 >= response.status_code >= 200:
    forecast = []
    data = response.json()
    #pprint(data)
    if not more: print(f"{data['city']['name']}, {countries.get(data['city']['country']).name}:")
    else: print(f"Advanced Weather in {data['city']['name']}, {countries.get(data['city']['country']).name}:")
    j = 0
    while j < days*4:
        i = data['list'][j]
        date = i['dt_txt'][:10]
        if date in forecast: j += 1;
        else:
          forecast.append(date)
          temp = i['main']['temp']
          description = i['weather'][0]['description'].capitalize()
          
          if not more:
            print(f"Forecast for {date}: {temp}°C, {description}\n")
            j += 1
          else:
            weather_main = i['weather'][0]['main']
            feels_like = i['main']['feels_like']
            temp_min = i['main']['temp_min']
            temp_max = i['main']['temp_max']
            pressure = i['main']['pressure']
            humidity = i['main']['humidity']
            print(f"Forecast for {date}:")
            print(f"\n\nMax Temperature: {temp_max}°C\nMin Temperature: {temp_min}°C\nFeels Like: {feels_like}°C")
            print(f"\n\nWeather condition is {weather_main}, {description}.")
            print(f"\n\nOther weather information:\nPressure: {pressure}\nHumidity: {humidity}")
            print("\n\nPress [N] to go to the next date or [B] to go to the previous date.")
            while True:
              if keyboard.is_pressed("n"):
                keyboard.press("backspace")
                time.sleep(0.5)
                clear()
                j += 1
                break
              elif keyboard.is_pressed("b"):
                keyboard.press("backspace")
                time.sleep(0.5)
                clear()
                j -= 1
                break
            
    return 1
  elif 599 >= response.status_code >= 500:
    print("Error: Server is malfunctioning!")
  elif 499 >= response.status_code >= 400:
    print("Error: User fault! Please check city name and api key!")
  else:
    print("Error: Unknown Error occurred! Please copy the api response and create " \
          "a GitHub bug report.\nError Code: ", response.json)
  return -1


def get_weather(city: str, more=False) -> int: 
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
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
      return 1
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


def main():
  print(yellow("Press the required key. Press [H] for help"))
  while True:
    if keyboard.is_pressed("H"):
      clear()
      print(green("Press [C] to check weather for a city.\nPress [W] to get a 5 day forecast for a city.\nPress [H] for help\nPress [E] to quit."))
      keyboard.press("backspace")
      time.sleep(0.5)
    elif keyboard.is_pressed("e"):
      clear()
      keyboard.press("backspace")
      break
    elif keyboard.is_pressed("C"):
      clear()
      keyboard.press("backspace")
      city = input("City Name: ")
      err = get_weather(city=city)
      if err > 0:
        print(yellow("Press [M] for more information or [H] to go to Home."))
        while True:
          if keyboard.is_pressed("m"):
            keyboard.press("backspace")
            clear()
            get_weather(city=city, more=True)
            print(yellow("Press [H] to go to Home."))
          elif keyboard.is_pressed("h"):
            keyboard.press("backspace")
            clear()
            time.sleep(0.5)
            break
      print(yellow("Press the required key. Press [H] for help"))
    elif keyboard.is_pressed("w"):
      clear()
      keyboard.press("backspace")
      city = input("City Name: ")
      try:
        days = int(input("Number of days to forecast: "))
        if days > 5:
          print(red("Resorting to the maximum (5 days)."))
          days = 10
        elif days < 1:
          print(red("Resorting to the minimum (1 day)."))
          days = 1
      except Exception:
        print(red("Invalid input! Resorting to the default (5 days)."))
        days = 5
      err = get_future_forecast(city=city, days=days)
      if err > 0:
        print(yellow("Press [M] for more information or [H] to go to Home."))
        while True:
          if keyboard.is_pressed("m"):
            keyboard.press("backspace")
            clear()
            get_future_forecast(city=city, days=days, more=True)
            break
          elif keyboard.is_pressed("h"):
            keyboard.press("backspace")
            clear()
            time.sleep(0.5)
            break
      print(yellow("Press the required key. Press [H] for help"))

if __name__ == "__main__":
  print(yellow("Welcome to Weather API!", ["bold", "underlined"]))
  main()