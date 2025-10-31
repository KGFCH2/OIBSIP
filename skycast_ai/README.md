# SkyCast AI - Intelligent Real-Time Weather Forecasting App

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

## Deployment on Streamlit Cloud

1. **Push your code** to GitHub (this repo).
2. **Go to [share.streamlit.io](https://share.streamlit.io)**.
3. **Connect your GitHub account** and select the `OIBSIP` repository.
4. **Set the main file path** to `skycast_ai/app.py`.
5. **Add your OpenWeatherMap API key** in the app secrets:
   - Go to app settings > Secrets
   - Add: `OPENWEATHER_API_KEY = "your_api_key_here"`
6. **Deploy!**

## Local Development

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