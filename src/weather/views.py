import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a8ddfcdf6189dc4c720b27c1ddcff18c'
    err_msg = ' '
    message = ' '
    message_class = ' '

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exists in the world'
            else:
                err_msg = ' City already exits in the Database'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City have added successfully'
            message_class = 'is-success'

    print(err_msg)

    form = CityForm
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']

        }
        weather_data.append(city_weather)
    print(weather_data)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'weather/index.html', context)
