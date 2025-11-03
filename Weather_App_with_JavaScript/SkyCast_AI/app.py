import streamlit as st
import requests
import datetime
import plotly.express as px
from geopy.geocoders import Nominatim

# Function to get current weather
def get_weather(city, api_key, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get 5-day forecast
def get_forecast(city, api_key, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to auto-detect city from IP
def get_city_from_ip():
    try:
        response = requests.get("http://ipinfo.io/json")
        data = response.json()
        return data.get('city', None)
    except:
        return None

# -------------------------
# WeatherAPI.com helpers
# -------------------------
def get_weather_weatherapi(city, api_key, units='metric'):
    """Return a normalized dict similar to OpenWeatherMap current weather structure.
    This allows reusing the existing display logic with minimal branching.
    """
    # Fetch current and 1-day forecast (for sunrise/sunset)
    try:
        cur_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        resp = requests.get(cur_url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()

        # Get sunrise/sunset from forecast endpoint (1 day)
        fore_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no&alerts=no"
        fore_resp = requests.get(fore_url, timeout=10)
        sunrise_ts = None
        sunset_ts = None
        if fore_resp.status_code == 200:
            fore = fore_resp.json()
            fd0 = fore.get('forecast', {}).get('forecastday', [])
            if fd0:
                astro = fd0[0].get('astro', {})
                date = fd0[0].get('date')
                # astro times like "06:12 AM" and date like '2023-09-01'
                try:
                    if astro.get('sunrise'):
                        dt_sr = datetime.datetime.strptime(f"{date} {astro['sunrise']}", "%Y-%m-%d %I:%M %p")
                        sunrise_ts = int(dt_sr.timestamp())
                    if astro.get('sunset'):
                        dt_ss = datetime.datetime.strptime(f"{date} {astro['sunset']}", "%Y-%m-%d %I:%M %p")
                        sunset_ts = int(dt_ss.timestamp())
                except Exception:
                    sunrise_ts = None
                    sunset_ts = None

        current = data.get('current', {})
        # normalize to OpenWeatherMap-like structure
        temp = current.get('temp_c') if units == 'metric' else current.get('temp_f')
        feels = current.get('feelslike_c') if units == 'metric' else current.get('feelslike_f')
        pressure = current.get('pressure_mb')  # hPa
        wind_speed = current.get('wind_kph') if units == 'metric' else current.get('wind_mph')
        wind_deg = current.get('wind_degree', 0)
        humidity = current.get('humidity')
        description = current.get('condition', {}).get('text', '')
        icon = current.get('condition', {}).get('icon', '')

        normalized = {
            'main': {
                'temp': temp,
                'feels_like': feels,
                'humidity': humidity,
                'pressure': pressure,
            },
            'wind': {
                'speed': wind_speed,
                'deg': wind_deg,
            },
            'weather': [
                {
                    'description': description,
                    'icon': icon.replace('//', 'https://') if icon else ''
                }
            ],
            'sys': {
                'sunrise': sunrise_ts,
                'sunset': sunset_ts,
            }
        }
        return normalized
    except Exception:
        return None


def get_forecast_weatherapi(city, api_key, units='metric'):
    """Return a normalized forecast dict with a 'list' key where each item resembles OpenWeatherMap 3-hour entries.
    We'll combine hourly data across forecast days and sample every 3 hours to approximate the 3-hour steps.
    """
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5&aqi=no&alerts=no"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        forecast_days = data.get('forecast', {}).get('forecastday', [])
        combined_hours = []
        for day in forecast_days:
            # each 'hour' entry has time_epoch and temp_c/temp_f
            for h in day.get('hour', []):
                combined_hours.append(h)

        # Sample every 3 hours to mimic OpenWeatherMap 3h granularity
        sampled = []
        for i in range(0, len(combined_hours), 3):
            h = combined_hours[i]
            dt = h.get('time_epoch')
            temp = h.get('temp_c') if units == 'metric' else h.get('temp_f')
            humidity = h.get('humidity')
            desc = h.get('condition', {}).get('text', '')
            icon = h.get('condition', {}).get('icon', '')
            sampled.append({
                'dt': dt,
                'main': {
                    'temp': temp,
                    'humidity': humidity,
                },
                'weather': [
                    {
                        'description': desc,
                        'icon': icon.replace('//', 'https://') if icon else ''
                    }
                ]
            })

        return {'list': sampled}
    except Exception:
        return None

# Streamlit app
st.set_page_config(page_title="SkyCast AI", page_icon="🌦️")

st.title("🌦️ SkyCast AI - Intelligent Weather Dashboard")

# Provider selection (OpenWeatherMap or WeatherAPI.com)
provider = st.selectbox("Select weather provider", ["OpenWeatherMap", "WeatherAPI.com"])

# API Key input
api_label = "Enter your API Key for OpenWeatherMap" if provider == "OpenWeatherMap" else "Enter your API Key for WeatherAPI.com"
api_key = st.text_input(api_label, type="password")
if not api_key:
    st.warning("Please enter your API key to continue.")
    st.stop()

# Units selection
units = st.selectbox("Select temperature unit", ["metric", "imperial"])
unit_symbol = "°C" if units == "metric" else "°F"

# Location input
location_option = st.radio("How would you like to select location?", ("Enter City", "Auto-detect from IP"))

city = None
if location_option == "Enter City":
    city = st.text_input("Enter city name")
elif location_option == "Auto-detect from IP":
    city = get_city_from_ip()
    if city:
        st.success(f"Detected city: {city}")
    else:
        st.error("Could not detect your location. Please enter city manually.")
        city = st.text_input("Enter city name")

if city:
    # Fetch current weather depending on provider
    if provider == "OpenWeatherMap":
        weather_data = get_weather(city, api_key, units)
        forecast_data = get_forecast(city, api_key, units)
    else:
        weather_data = get_weather_weatherapi(city, api_key, units)
        forecast_data = get_forecast_weatherapi(city, api_key, units)

    if weather_data:
        st.subheader("🌡️ Current Weather")

        # Extract data (normalized for both providers)
        temp = weather_data['main'].get('temp')
        feels_like = weather_data['main'].get('feels_like')
        humidity = weather_data['main'].get('humidity')
        pressure = weather_data['main'].get('pressure')
        wind_speed = weather_data['wind'].get('speed')
        wind_deg = weather_data['wind'].get('deg', 0)
        description = weather_data['weather'][0].get('description', '').capitalize()
        icon_code = weather_data['weather'][0].get('icon', '')

        # Display weather icon
        if provider == "OpenWeatherMap":
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        else:
            # WeatherAPI returns icon URLs already
            icon_url = icon_code if icon_code.startswith('http') else icon_code

        if icon_url:
            st.image(icon_url, width=100)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{temp}{unit_symbol}")
            st.metric("Feels Like", f"{feels_like}{unit_symbol}")
        with col2:
            st.metric("Humidity", f"{humidity}%")
            st.metric("Pressure", f"{pressure} hPa" if pressure else "N/A")
        with col3:
            # For consistency, present wind speed with units
            wind_unit = "kph" if units == 'metric' else 'mph'
            st.metric("Wind Speed", f"{wind_speed} {wind_unit}")
            st.write(f"Wind Direction: {wind_deg}°")

        st.write(f"**Condition:** {description}")

        # Sunrise/Sunset (may be None for some providers)
        sr_ts = weather_data.get('sys', {}).get('sunrise')
        ss_ts = weather_data.get('sys', {}).get('sunset')
        if sr_ts:
            try:
                sunrise = datetime.datetime.fromtimestamp(sr_ts)
                st.write(f"🌅 Sunrise: {sunrise.strftime('%H:%M')}")
            except Exception:
                pass
        if ss_ts:
            try:
                sunset = datetime.datetime.fromtimestamp(ss_ts)
                st.write(f"🌇 Sunset: {sunset.strftime('%H:%M')}")
            except Exception:
                pass

    # Fetch forecast and plot
    if forecast_data:
        st.subheader("📈 5-Day Weather Forecast")

        # Process forecast data
        forecast_list = forecast_data.get('list', [])
        dates = []
        temps = []
        humidities = []
        descriptions = []
        icons = []

        for item in forecast_list:
            # dt may already be epoch (WeatherAPI) or seconds (OpenWeatherMap)
            dt_val = item.get('dt')
            try:
                dt = datetime.datetime.fromtimestamp(dt_val)
            except Exception:
                dt = None
            dates.append(dt)
            temps.append(item['main'].get('temp'))
            humidities.append(item['main'].get('humidity'))
            descriptions.append(item['weather'][0].get('description', '').capitalize())
            icons.append(item['weather'][0].get('icon', ''))

        # Temperature forecast chart (filter out None dates)
        fig = px.line(x=[d for d in dates if d is not None], y=[t for d, t in zip(dates, temps) if d is not None], title="Temperature Forecast", labels={'x': 'Date', 'y': f'Temperature ({unit_symbol})'})
        st.plotly_chart(fig)

        # Display forecast in a table or cards
        st.subheader("Detailed Forecast")
        for i in range(0, len(forecast_list), 8):  # Every ~24 hours
            day_data = forecast_list[i]
            dt_val = day_data.get('dt')
            try:
                dt = datetime.datetime.fromtimestamp(dt_val)
                dt_str = dt.strftime('%A, %d %b')
            except Exception:
                dt_str = ''
            temp = day_data['main'].get('temp')
            desc = day_data['weather'][0].get('description', '').capitalize()
            icon = day_data['weather'][0].get('icon', '')

            # Build icon_url depending on provider
            if provider == "OpenWeatherMap":
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            else:
                icon_url = icon if icon.startswith('http') else icon

            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                if icon_url:
                    st.image(icon_url, width=50)
            with col2:
                st.write(f"**{dt_str}**")
                st.write(f"{temp}{unit_symbol}")
            with col3:
                st.write(desc)
            st.markdown("---")

else:
    st.info("Please enter a city name to get weather information.")

st.markdown("---")
st.write("Data provided by your selected provider. For OpenWeatherMap get a free API key at [openweathermap.org](https://openweathermap.org/api), for WeatherAPI get one at [weatherapi.com](https://www.weatherapi.com/)")