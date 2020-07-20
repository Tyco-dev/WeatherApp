from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import requests
from .models import City
from .forms import CityForm


# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a6cc412a44a9c70445459c11fda9940f'

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    error_message = 'City does not exist, atleast on Earth...'
            else:
                error_message = 'You already added this city!'

        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City has been added'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    city = City.objects.get(name=city_name)
    city.delete()
    return redirect('index')