import requests, pytz; from iso3166 import countries; from datetime import datetime; from simple_colors import *; from os import system, name


api_key = "ede8ff9e889a72caabf0bcec094eb623"


def save_to_history(query: str, data: dict):
  """
  Updates the global history dictionary by incrementing the number of queries 
  and adding the query string and data to the dictionary.
  
  Args:
    query (str): The user query string
    data (dict): The data associated with the query
  """

  global history, number_of_queries
  number_of_queries += 1
  history[str(number_of_queries) + ". " + query] = data


def clear():
  """
  Clears the terminal screen.
  Checks the current operating system and calls the appropriate 
  system command to clear the terminal screen - 'cls' for Windows
  or 'clear' for Linux/macOS.
  """

  # for windows
  if name == 'nt':
    _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')


def deg_to_compass(degrees):
  """
  Validates that input degrees are between 0 and 360, then maps 
  the degrees to a compass direction by indexing into a lookup
  table of directions.
  
  Args:
    degrees: The degrees to map to a compass direction
  
  Returns:
    A string representing the compass direction
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


def clean_data(data, query: str, multiple_days=True):
  """
  Processes weather data from the OpenWeatherMap API into a more convenient format.
  
  If multiple_days is True, retrieves forecast data for multiple days and returns a list of dictionaries containing the processed daily weather data. 
  
  If multiple_days is False, retrieves current weather data and returns a dictionary containing the processed current weather data.
  
  Saves the processed weather data to the query history.
  
  Args:
    data: A dictionary containing the raw weather data from the OpenWeatherMap API.
    query: The city that the data is associated with.
    multiple_days: Whether the output needs to be a list or dict
    
  Returns:
    A list of dictionaries containing the processed daily weather data if multiple_days is True, otherwise a dictionary containing the processed current weather data.
  """
  
  if multiple_days:
    forecast = []
    data_output = []
    for i in data['list']:
        date = i['dt_txt'][:10]
        if date not in forecast:
          forecast.append(date)
          data_output.append({})
          data_output[-1]["city"] = data['city']['name']
          data_output[-1]["country"] = data['city']['country']
          data_output[-1]["date"] = date
          data_output[-1]["temp"] = i['main']['temp']
          data_output[-1]["description"] = i['weather'][0]['description'].capitalize()
          
          data_output[-1]["weather_main"] = i['weather'][0]['main']
          data_output[-1]["feels_like"] = i['main']['feels_like']
          data_output[-1]["temp_min"] = i['main']['temp_min']
          data_output[-1]["temp_max"] = i['main']['temp_max']
          data_output[-1]["pressure"] = i['main']['pressure']
          data_output[-1]["humidity"] = i['main']['humidity']
    save_to_history(query=query, data=data_output)
    return data_output
  data_output = {}
  data_output["city"] = data['name']
  data_output["country"] = data['sys']['country']
  data_output["temp"] = data['main']['temp']
  data_output["description"] = data['weather'][0]['description'].capitalize()
  data_output["weather_main"] = data['weather'][0]['main']
  data_output["feels_like"] = data['main']['feels_like']
  data_output["temp_min"] = data['main']['temp_min']
  data_output["temp_max"] = data['main']['temp_max']
  data_output["pressure"] = data['main']['pressure']
  data_output["humidity"] = data['main']['humidity']
  data_output["visibility"] = data['visibility']
  data_output["wind_speed"] = data['wind']['speed']
  data_output["wind_direction"] = deg_to_compass(data['wind']['deg'])
  data_output["sunset"] = unix_time_to_datetime(data['sys']['sunset'], timezone=pytz.timezone("Australia/Sydney"))
  data_output["sunrise"] = unix_time_to_datetime(data['sys']['sunrise'], timezone=pytz.timezone("Australia/Sydney"))
  save_to_history(query=query, data=data_output)
  return data_output


def get_future_forecast(city: str, more=False) -> int:
  """
  Makes an API request to the OpenWeatherMap API to get a 6 day weather data for the given city. 
  
  Handles API response codes to detect errors or lack of internet connectivity.
  Prints appropriate error messages on failure.
  
  On success, calls clean_data() to parse API response, print_weather() 
  to print weather info, and returns 1.

  Args:
    city: Name of city to get forecast for
    more: Whether to show advanced forecast details 
  
  Returns:
    int: 1 for success, -1 for error
  """
  try:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if 299 >= response.status_code >= 200:
      data = response.json()
      n_data = clean_data(data, query=city)
      if not more:
        for i in range(len(n_data)):
          print(f"Forecast for {n_data[i]['date']}:")
          print(f"{data['city']['name']}, {countries.get(data['city']['country']).name}: {n_data[i]['temp']}°C, {n_data[i]['description']}\n")
        return 1
      else: 
        print(f"Advanced Weather in {data['city']['name']}, {countries.get(data['city']['country']).name}:")
        j = 0
        while True:
          print(f"Forecast for {n_data[j]['date']}:")
          print(f"\n\nMax Temperature: {n_data[j]['temp_max']}°C\nMin Temperature: {n_data[j]['temp_min']}°C\nFeels Like: {n_data[j]['feels_like']}°C")
          print(f"\n\nWeather condition is {n_data[j]['weather_main']}, {n_data[j]['description']}.")
          print(f"\n\nOther weather information:\nPressure: {n_data[j]['pressure']}\nHumidity: {n_data[j]['humidity']}")
          text = input(yellow("\n\nEnter [N] to go to the next date or [B] to go to the previous date or anything else to go back: "))
          if text.lower() == "n":
            clear()
            if j == len(n_data) - 1:
              j = 0
            else:
              j += 1
          elif text.lower() == "b":
            clear()
            if j == 0:
              j = len(n_data) - 1
            else:
              j -= 1
          else:
            return 1
    elif 599 >= response.status_code >= 500:
      print(red("Error: Server is malfunctioning!"), "bold")
    elif 499 >= response.status_code >= 400:
      print(red("Error: User fault! Please check city name and api key!", "bold"))
    else:
      print(red(("Error: Unknown Error occurred! Please copy the api response and create " \
            "a GitHub bug report.\nError Code: ", response.json), "bold"))
  except Exception:
    print(red("Error: No Internet Connection!"), "bold")
  return -1


def print_weather(data, more=False):
  """
  Parses weather data from API response into readable format.
  
  Args:
    data: Cleaned weather API response data
    more: Whether to print advanced information
  """
  city = data['city']
  country = data['country']
  temp = data['temp']
  description = data['description'].capitalize()
  weather_main = data['weather_main']
  feels_like = data['feels_like']
  temp_min = data['temp_min']
  temp_max = data['temp_max']
  pressure = data['pressure']
  humidity = data['humidity']
  try:
    visibility = data['visibility']
    wind_speed = data['wind_speed']
    wind_direction = data['wind_direction']
    sunset = data['sunset']
    sunsrise = data['sunrise']
  except KeyError:
    visibility = "Not Available"
    wind_speed = "Not Available"
    wind_direction = "Not Available"
    sunset = "Not Available"
    sunsrise = "Not Available"
  if not more:
      print(f"Weather in {city}, {countries.get(country).name}: {temp}°C, {description}")
      return
  print(f"Advanced Weather in {city}, {countries.get(country).name}:")
  print(f"\n\nCurrent Temperature: {temp}°C\nFeels Like: {feels_like}°C\nMax Temperature: {temp_max}°C\nMin Temperature: {temp_min}°C")
  print(f"\n\nWeather condition is {weather_main}, {description}.")
  print(f"\n\nWind speed: {wind_speed} m/s\nWind Direction: {wind_direction}")
  print(f"\n\nSunrise: {sunsrise}\nSunset: {sunset}")
  print(f"\n\nOther weather information:\nPressure: {pressure}\nHumidity: {humidity}\nVisibility: {visibility}")


def get_weather(city, more=False) -> int:
  """
  Makes an API request to the OpenWeatherMap API to get weather data for the given city. 
  
  Handles API response codes to detect errors or lack of internet connectivity.
  Prints appropriate error messages on failure.
  
  On success, calls clean_data() to parse API response, print_weather() 
  to print weather info, and returns 1.
  
  Args:
    city: Name of city to get weather for
    more: Whether to print more detailed weather info
    
  Returns:
    int: 1 for success, -1 for failure
  """
  try:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if 299 >= response.status_code >= 200:
      data = clean_data(response.json(), query=city, multiple_days=False)
      print_weather(data=data, more=more)
      return 1
    elif 599 >= response.status_code >= 500:
      print(red("Error: Server is malfunctioning!", "bold"))
    elif 499 >= response.status_code >= 400:
      print(red("Error: User fault! Please check city name and api key!", "bold"))
    else:
      print(red(("Error: Unknown Error occurred! Please copy the api response and create " \
          "a GitHub bug report.\nError Code: ", response.json), "bold"))
  except Exception:
    print(red("Error: No Internet Connection!"), "bold")
  return -1


def main():
  """
  Provides an interactive command line interface for getting weather data.
  
  Allows the user to:
  - Get current weather for a city
  - Get a 6 day weather forecast for a city  
  - View previous search history
  - Get help/assistance
  
  """
  while True:
    text = input(yellow("Enter the required key. Enter [A] for assistance: "))
    if text.lower() == "a":
      clear()
      print(green("Enter [C] to check weather for a city.\nEnter [W] to get a 6 day forecast for a city.\nEnter [H] for search history\nEnter [A] for assistance\nEnter [E] to quit."))
    elif text.lower() == "e":
      clear()
      break
    elif text.lower() == "c":
      clear()
      city = input("City Name: ")
      err = get_weather(city=city)
      if err > 0:
        text = input(yellow("Enter [M] for more information or [H] to go to Home: "))
        if text.lower() == "m":
          clear()
          get_weather(city=city, more=True)
        elif text.lower() == "h":
          clear()
        else:
          print(red("Invalid Input! Resorting to default [H]!", "bold"))
    elif text.lower() == "w":
      clear()
      city = input("City Name: ")
      err = get_future_forecast(city=city)
      if err > 0:
        text = input(yellow("Enter [M] for more information or [H] to go to Home: "))
        if text.lower() == "m":
          clear()
          get_future_forecast(city=city, more=True)
        elif text.lower() == "h":
          clear()
        else:
          print(red("Invalid Input! Resorting to default [H]!", "bold"))
    elif text.lower() == "h":
      if history.keys():
        clear()
        j = 0
        while True:
          i = list(history.keys())[j]
          print(cyan(i , "bold"))
          if type(history[i]) == list:
            for k in (history[i]):
              print(cyan(k['date']))
              print_weather(k, more=True)
              print("\n")
          elif type(history[i]) == dict:
            print_weather(history[i], more=True)
          print("\n\n")
          text = input(yellow("Enter [N] to go to the next date or [B] to go to the previous date or anything else to go back: "))
          if text.lower() == "n":
            clear()
            if j == len(history.keys()) - 1:
              j = 0
            else:
              j += 1
          elif text.lower() == "b":
            clear()
            if j == 0:
              j = len(history.keys()) - 1
            else:
              j -= 1
          else:
            break
      else:
        clear()
        print(red("Nothing to show!"))


if __name__ == "__main__":
  """
  Initializes global variables to track state and prints a welcome message.
  
  history: Dictionary to store query history
  number_of_queries: Counter for number of queries made
  Prints welcome message and calls main() function.
  """
  history = {}
  number_of_queries = 0
  clear()
  print(yellow("Welcome to Weather API!", ["bold", "underlined"]))
  main()