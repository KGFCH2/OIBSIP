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

# Streamlit app
st.set_page_config(page_title="SkyCast AI", page_icon="🌦️")

st.title("🌦️ SkyCast AI - Intelligent Weather Dashboard")

# API Key input
api_key = st.secrets.get("OPENWEATHER_API_KEY") if "OPENWEATHER_API_KEY" in st.secrets else st.text_input("Enter your OpenWeatherMap API Key", type="password")
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
    # Fetch current weather
    weather_data = get_weather(city, api_key, units)
    if weather_data:
        st.subheader("🌡️ Current Weather")
        
        # Extract data
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind'].get('deg', 0)
        description = weather_data['weather'][0]['description'].capitalize()
        icon_code = weather_data['weather'][0]['icon']
        
        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url, width=100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{temp}{unit_symbol}")
            st.metric("Feels Like", f"{feels_like}{unit_symbol}")
        with col2:
            st.metric("Humidity", f"{humidity}%")
            st.metric("Pressure", f"{pressure} hPa")
        with col3:
            st.metric("Wind Speed", f"{wind_speed} km/h")
            st.write(f"Wind Direction: {wind_deg}°")
        
        st.write(f"**Condition:** {description}")
        
        # Sunrise/Sunset
        sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
        st.write(f"🌅 Sunrise: {sunrise.strftime('%H:%M')}")
        st.write(f"🌇 Sunset: {sunset.strftime('%H:%M')}")
    
    # Fetch forecast
    forecast_data = get_forecast(city, api_key, units)
    if forecast_data:
        st.subheader("📈 5-Day Weather Forecast")
        
        # Process forecast data
        forecast_list = forecast_data['list']
        dates = []
        temps = []
        humidities = []
        descriptions = []
        icons = []
        
        for item in forecast_list:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            dates.append(dt)
            temps.append(item['main']['temp'])
            humidities.append(item['main']['humidity'])
            descriptions.append(item['weather'][0]['description'].capitalize())
            icons.append(item['weather'][0]['icon'])
        
        # Temperature forecast chart
        fig = px.line(x=dates, y=temps, title="Temperature Forecast", labels={'x': 'Date', 'y': f'Temperature ({unit_symbol})'})
        st.plotly_chart(fig)
        
        # Display forecast in a table or cards
        st.subheader("Detailed Forecast")
        for i in range(0, len(forecast_list), 8):  # Every 24 hours (8 * 3h)
            day_data = forecast_list[i]
            dt = datetime.datetime.fromtimestamp(day_data['dt'])
            temp = day_data['main']['temp']
            desc = day_data['weather'][0]['description'].capitalize()
            icon = day_data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                st.image(icon_url, width=50)
            with col2:
                st.write(f"**{dt.strftime('%A, %d %b')}**")
                st.write(f"{temp}{unit_symbol}")
            with col3:
                st.write(desc)
            st.markdown("---")

else:
    st.info("Please enter a city name to get weather information.")

st.markdown("---")
st.write("Powered by OpenWeatherMap API. Get your free API key at [openweathermap.org](https://openweathermap.org/api)")