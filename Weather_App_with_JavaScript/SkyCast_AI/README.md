# SkyCast AI - Intelligent Real-Time Weather Forecasting App

**Note:** For deployment compatibility, the deployable version is now in the `SkyCast_ai` folder in the repository root.

Please use `SkyCast_ai/app.py` as the main file for Streamlit Cloud deployment.

SkyCast AI is a personalized atmospheric dashboard that fetches real-time weather data, forecasts, and visual insights using APIs. It evolves into an intelligent assistant that predicts patterns, gives advice, and alerts users to extreme weather.

## Features

- **Real-time Weather Data**: Current temperature, humidity, pressure, wind speed, and conditions.
- **5-Day Forecast**: Hourly forecasts with temperature trends and weather icons.
- **Auto Location Detection**: Detects user's city using IP address.
- **Unit Conversion**: Toggle between Celsius and Fahrenheit.
- **Interactive Visualizations**: Temperature forecast charts using Plotly.
- **Weather Icons**: Dynamic icons from OpenWeatherMap.

## Tech Stack

- **Python**
- **Streamlit** for GUI
- **Requests** for API calls
- **Plotly** for data visualization
- **Geopy** for geolocation (optional)
- **OpenWeatherMap API** for weather data

## Setup Instructions

1. **Clone or Download** the project files.

2. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Get API Key**:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api) and get a free API key.

4. **Run the App**:
   ```
   streamlit run app.py
   ```
   Or if streamlit is not in PATH:
   ```
   python -m streamlit run app.py
   ```

5. **Enter your API Key** in the app and select your location method.

## Usage

- Choose to enter a city manually or auto-detect via IP.
- View current weather conditions and 5-day forecast.
- Switch between temperature units.

## Future Enhancements

- AI-powered weather insights and predictions.
- Voice input and smart alerts.
- Interactive maps and mobile app version.

## License

This project is for educational purposes. Ensure compliance with API terms of service.
