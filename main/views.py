from django.shortcuts import render
# importing json to load json data 
import json
# requests for GET and POST to API's
import requests


# Request 
def index(request):
 
    if request.method == 'POST':
        #### Earth Weather ####
        city = request.POST['city']

        # source contains JSON data from API, api id removed for posting
        source_earth = requests.post(
            'http://api.openweathermap.org/data/2.5/weather?q='
            + city + '&units=imperial&appid=')
        
        # converting JSON data to a dictionary
        list_of_data_earth = source_earth.json()

        # We are gonna round the temperature to the nearest whole number
        # earth_temp_rounded = round(list_of_data_earth['main']['temp']) 

        # data for variable list_of_data_earth
        earth_data = {
            "country_code": str(list_of_data_earth['sys']['country']),
        #    "earth_temp": str(earth_temp_rounded) + ' f',
            "earth_temp": str(list_of_data_earth['main']['temp']),
            "earth_pressure": str(list_of_data_earth['main']['pressure']),
            "earth_humidity": str(list_of_data_earth['main']['humidity'])
        }

               #### Mars Weather ####

            # mars_api_key, removed for publishing 
        mars_api_key = ''

        # source contains JSON data from API
        source_mars = requests.get(
            'https://api.nasa.gov/insight_weather/?api_key='
            + mars_api_key + '&feedtype=json&ver=1.0')

        # conver JSON data to a dictionary
        list_of_data_mars = source_mars.json()

        # days on Mars are called Sols, sol_keys are [0] - [6]
        # [6] is the most recent day, so we will be putting [6] into
        # this variable so we can call it into mars_data to get its data
        today_sol = str(list_of_data_mars['sol_keys'][6])

        # This variable is a converted form of the temperature given by the Insight API
        # we are converting from Celsius to Fahrenheit, and then rounding it to an intenger
        mars_temp_f = round((list_of_data_mars[today_sol]['AT']['av']) * 1.80 + 32)

        # data for variable list_of_data_mars
        mars_data = {
            # AT is for atmospheric temperature, but that is broken up into several other units
            # av is the average of all the daily readings, mn is the minimum, and mx is the maximum temp
            "mars_temp": str(mars_temp_f) + ' f',
            "todays_sol": str(list_of_data_mars['sol_keys'][6])
        }
    
    
    else:
        earth_data = {}
        mars_data = {}

    # return render(request, "main/index.html", earth_data, mars_data)
    return render(request, "main/index.html", {**mars_data, **earth_data})

    