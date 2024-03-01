import requests
from iso3166 import countries

#region
api_key = "ede8ff9e889a72caabf0bcec094eb623"
#endregion

city = input("City Name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# Send GET request and handle response
response = requests.get(url)
print(response.json(), "\n\n\n")
if response.status_code == 200:
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
  wind_direction = data['wind']['deg']  #TODO: Convert to North East South West
  #wind_gust = data['wind']['gust']  #TODO: Understand this!!! ! THIS WONT ALWAYS BE THE CASE!
  #! Clouds = [] ! THIS WONT ALWAYS BE THE CASE!
  sunset = data['sys']['sunset'] #TODO: Learn this !!!!
  sunsrise = data['sys']['sunrise'] #TODO: Learn this !!!!
  print(f"Weather in {city}, {countries.get(country).name}: {temp}°C, {description}")
else:
  print("Error: Could not retrieve weather data.")


def main():
  pass

if __name__ == "__main__":
  main()