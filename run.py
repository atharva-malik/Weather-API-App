from flask import Flask, render_template, request
from email_validator import validate_email
THIS !!!! !!!!! is_valid = validate_email('example@foasdccvo.com', check_deliverability=True)
import requests

app = Flask(__name__)

#region
"""
api_key = "ede8ff9e889a72caabf0bcec094eb623"


city = 'London'

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# Send GET request and handle response
response = requests.get(url)
print(response)
if response.status_code == 200:
  data = response.json()
  temp = data['main']['temp']
  description = data['weather'][0]['description'].capitalize()
  print(f"Weather in {city}: {temp:.2f}°C, {description}")
else:
  print("Error: Could not retrieve weather data.")
"""
#endregion


@app.route("/", methods = ['POST', 'GET'])
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    # Your logic to handle form submission (e.g., validate data, save to database)
    return str("ASdasdf")
  return render_template('signup.html')

if __name__ == "__main__":
    print(is_valid.normalized)
    app.run(debug=True)