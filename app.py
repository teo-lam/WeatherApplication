from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

# Define the Weather model
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    sunrise = db.Column(db.String(10), nullable=False)
    sunset = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    invalid_city_message = ''
    if request.method == 'POST':
        # select city from template
        city = request.form['city']
        api_key = 'f1151c74dae240f998a224912240808'
        # add key and city to url
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3'
        response = requests.get(url)
        if response.status_code == 200:
            # format reponse to json
            weather_data = response.json()
            print('new request', weather_data)
            for forecastday in weather_data['forecast']['forecastday']:
                date = datetime.strptime(forecastday['date'], '%Y-%m-%d').date()
                max_temp = forecastday['day']['maxtemp_c']
                min_temp = forecastday['day']['mintemp_c']
                precipitation = forecastday['day']['totalprecip_mm']
                sunrise = forecastday['astro']['sunrise']
                sunset = forecastday['astro']['sunset']
                condition = forecastday['day']['condition']['text']

                # Check if the record already exists
                existing_record = Weather.query.filter_by(city=city, date=date).first()
                if existing_record:
                    print('exisiting record', city)
                    # Update the existing record
                    existing_record.max_temp = max_temp
                    existing_record.min_temp = min_temp
                    existing_record.precipitation = precipitation
                    existing_record.sunrise = sunrise
                    existing_record.sunset = sunset
                    existing_record.condition = condition
                else:
                    # Add a new record
                    print('new record', city)
                    new_weather = Weather(
                        city=city,
                        date=date,
                        max_temp=max_temp,
                        min_temp=min_temp,
                        precipitation=precipitation,
                        sunrise=sunrise,
                        sunset=sunset,
                        condition=condition
                    )
                    db.session.add(new_weather)

                db.session.commit()
        else:
            invalid_city_message =  response.json()['error']['message'];
            weather_data = None

    return render_template('index.html', weather=weather_data, invalid_city_message=invalid_city_message)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)


