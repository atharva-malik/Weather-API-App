# Year 10 Assessment Task 1

This is a simple implementation of [OpenWeatherMap's] free weather api. It comes with a variety of features like, CLI interface, advanced or simple weather forecasts, multiple day forecast, search history, intuitive and clean interface, etcetera. It is fully functional and extremely easy to use!


## Features

- Easy to use
- Thoroughly commented and easily editable python code 
- Comes with basic CLI interface
- 6 Day Weather Forecast
- Single day weather forecast
- Search history
- Advanced/Simple weather forecast

## Technologies Used

This console application uses 2 main technologies on the front end, [Python 3.11] and the [simple-colors] module, but uses lots of different technologies in the background like the iso3166 module (to convert the default api country codes to a more readable form) and Pytz (to help convert time to different time zones)

## Installation

Install the repository and the following packages and you are good to go!
```sh
pip3 install -r .\requirements.txt
```

## Execution

To run the code, navigate to the directory of installation. Open the file 'main.py' and update line 10 to include your OpenWeatherMap API key. Close the file. Lastly, open the directory of installation in a terminal and type:
```sh
py -3 main.py
```
Then enter "A" to reach the Assistance Menu, allowing you to see the different commands available.

## Development

Want to contribute? Great! Pull requests and issues are welcome! [Here] is an excellent guide on how to create pull requests and forks to request changes. I suggest using the addon "Better Comments" on Visual Studio Code as it makes the comments more readable. If you can not use the addon, I have used the following tags to make the comments more readable:

- #!: This is a warning
- #*: This is used for in-line comments
- """

  """ This is a docstring, explaining the functions' use, arguments, and returns, if any.

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)
   [OpenWeatherMap's]: <https://openweathermap.org/api>
   [Python 3.11]: <https://www.python.org/downloads/release/python-3115/>
   [simple-colors]: <https://pypi.org/project/simple-colors/>
   [Here]: <https://www.dataschool.io/how-to-contribute-on-github/>
   [flask]: <https://pypi.org/project/Flask/>


### Credits
OpenWeatherMap for api key.
