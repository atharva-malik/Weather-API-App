import requests, time, pytz; from iso3166 import countries; from datetime import datetime; from simple_colors import *; from os import system, name

#region
api_key = "ede8ff9e889a72caabf0bcec094eb623"
#endregion


def save_to_history(query: str, data: dict):
  pass


def clear():
  # for windows
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')


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


def clean_data(data):
  forecast = []
  data_output = []
  for i in data['list']:
      date = i['dt_txt'][:10]
      if date not in forecast:
        forecast.append(date)
        data_output.append({})
        data_output[-1]["date"] = date
        data_output[-1]["temp"] = i['main']['temp']
        data_output[-1]["description"] = i['weather'][0]['description'].capitalize()
        
        data_output[-1]["weather_main"] = i['weather'][0]['main']
        data_output[-1]["feels_like"] = i['main']['feels_like']
        data_output[-1]["temp_min"] = i['main']['temp_min']
        data_output[-1]["temp_max"] = i['main']['temp_max']
        data_output[-1]["pressure"] = i['main']['pressure']
        data_output[-1]["humidity"] = i['main']['humidity']
  return data_output


def get_future_forecast(city: str, more=False) -> int:
  url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
  response = requests.get(url)
  if 299 >= response.status_code >= 200:
    data = response.json()
    n_data = clean_data(data)
    if not more: print(f"{data['city']['name']}, {countries.get(data['city']['country']).name}: {n_data[0]['temp']}°C, {n_data[0]['description']}"); return 1
    else: 
      print(f"Advanced Weather in {data['city']['name']}, {countries.get(data['city']['country']).name}:")
      j = 0
      while True:
        if j < 0:
          break
        print(f"Forecast for {n_data[j]['date']}:")
        print(f"\n\nMax Temperature: {n_data[j]['temp_max']}°C\nMin Temperature: {n_data[j]['temp_min']}°C\nFeels Like: {n_data[j]['feels_like']}°C")
        print(f"\n\nWeather condition is {n_data[j]['weather_main']}, {n_data[j]['description']}.")
        print(f"\n\nOther weather information:\nPressure: {n_data[j]['pressure']}\nHumidity: {n_data[j]['humidity']}")
        text = input("\n\nEnter [N] to go to the next date or [B] to go to the previous date or anything else to go back: ")
        if text.lower() == "n":
          time.sleep(0.5)
          clear()
          if j == len(n_data) - 1:
            j = 0
          else:
            j += 1
        elif text.lower() == "b":
          time.sleep(0.5)
          clear()
          if j == 0:
            j = len(n_data) - 1
          else:
            j -= 1
        else:
          j = -1
          return 1
    return 1
  elif 599 >= response.status_code >= 500:
    print("Error: Server is malfunctioning!")
  elif 499 >= response.status_code >= 400:
    print("Error: User fault! Please check city name and api key!")
  else:
    print("Error: Unknown Error occurred! Please copy the api response and create " \
          "a GitHub bug report.\nError Code: ", response.json)
  return -1


def print_weather(data, more=False):
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
  wind_direction = deg_to_compass(data['wind']['deg'])
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


def get_weather(city="", more=False, data={}) -> int: 
  if data == {}:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if 299 >= response.status_code >= 200:
      data = response.json()
      print_weather(data=data, more=more)
    elif 599 >= response.status_code >= 500:
      print("Error: Server is malfunctioning!")
    elif 499 >= response.status_code >= 400:
      print("Error: User fault! Please check city name and api key!")
    else:
      print("Error: Unknown Error occurred! Please copy the api response and create " \
            "a GitHub bug report.\nError Code: ", response.json)
    return -1


def main():
  while True:
    text = input(yellow("Enter the required key. Enter [A] for assistance: "))
    if text.lower() == "a":
      clear()
      print(green("Press [C] to check weather for a city.\nPress [W] to get a 5 day forecast for a city.\nPress [H] for search history\nEnter [A] for assistance\nPress [E] to quit."))
    elif text.lower() == "e":
      clear()
      break
    elif text.lower() == "c":
      clear()
      city = input("City Name: ")
      err = get_weather(city=city)
      if err > 0:
        text = input(yellow("Enter [M] for more information or [H] to go to Home."))
        if text.lower() == "m":
          clear()
          get_weather(city=city, more=True)
          print(yellow("Enter [H] to go to Home."))
        elif text.lower() == "h":
          clear()
        else:
          print(red("Invalid Input! Resorting to default [H]!", "bold"))
    elif text.lower() == "w":
      clear()
      city = input("City Name: ")
      err = get_future_forecast(city=city)
      if err > 0:
        text = input(yellow("Press [M] for more information or [H] to go to Home: "))
        if text.lower() == "m":
          clear()
          get_future_forecast(city=city, more=True)
        elif text.lower() == "h":
          clear()
          time.sleep(0.5)
        else:
          print(red("Invalid Input! Resorting to default [H]!", "bold"))
      clear()
    elif text.lower() == "h":
      for i in range(len(history.keys())):
        print(i)
        clear()

if __name__ == "__main__":
  history = {}
  clear()
  print(yellow("Welcome to Weather API!", ["bold", "underlined"]))
  main()