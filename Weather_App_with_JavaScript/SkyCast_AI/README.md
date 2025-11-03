# SkyCast AI — Intelligent Real-Time Weather Dashboard

This repository provides the SkyCast AI weather dashboard. The deployable app lives in the `SkyCast_AI` folder at the repository root. Use `SkyCast_AI/app.py` as the entry point for Streamlit deployments.

SkyCast AI fetches real-time weather and forecast data, visualizes trends, and can be extended with AI-driven insights and alerts.

## Key features

- Real-time current weather (temperature, humidity, pressure, wind, conditions)
- Hourly / multi-day forecast with interactive charts
- Auto-location detection (IP-based) and manual city input
- Unit toggle (Celsius / Fahrenheit)
- Plotly visualizations and OpenWeatherMap icons

## Supported providers

- OpenWeatherMap (default): current + 5-day/3-hour forecast endpoints are used when this provider is selected.
- WeatherAPI.com: supported as an alternative provider; the app normalizes WeatherAPI responses so the UI can reuse the same display logic (current + sampled forecast entries).

Note: When using WeatherAPI the app samples hourly data (every ~3 hours) to approximate OpenWeatherMap's 3-hour forecast granularity.

## Tech stack

- Python 3.8+
- Streamlit (UI)
- requests (HTTP)
- plotly (charts)
- Optional: geopy for enhanced geolocation
- OpenWeatherMap API for weather data

Other runtime notes:
- The app uses ipinfo.io (via a simple GET request) to auto-detect city from the user's IP when "Auto-detect from IP" is chosen.
- The repository's `app.py` currently imports `geopy.geocoders.Nominatim` but geopy is optional; the IP detect path doesn't require geopy.

## Quick setup

1. Clone or download the repository.

2. Create and activate a virtual environment (recommended):

   Windows (cmd.exe):
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

4. Set your OpenWeatherMap API key. You can set an environment variable or enter it in the app when prompted.

   Windows (cmd.exe):
   ```cmd
   setx OPENWEATHER_API_KEY "your_api_key_here"
   ```

   If you plan to use WeatherAPI.com as the provider, set:

   ```cmd
   setx WEATHERAPI_KEY "your_weatherapi_key_here"
   ```

   Note: After running setx you may need to open a new terminal or restart your editor to see the variable.


5. Run the Streamlit app (use the app in `SkyCast_AI`):

   ```cmd
   cd SkyCast_AI
   streamlit run app.py
   ```

   Or, if streamlit is not on PATH:

   ```cmd
   python -m streamlit run app.py
   ```

## Where to find the deployable app

The deployable Streamlit app is located at:

 - `SkyCast_AI/app.py` — main app for deployment and local run

If you see an older `app.py` at the repository root, prefer the one in `SkyCast_AI` for current deployment compatibility.

## Configuration & usage notes

- API key: The app uses the OpenWeatherMap API. Provide a valid API key through the UI or via the `OPENWEATHER_API_KEY` environment variable.
- If you select WeatherAPI.com as the provider, provide a WeatherAPI key via the UI or the `WEATHERAPI_KEY` environment variable.
- Location: Choose between manual city input or auto-detection (IP). Auto-detection can be less accurate depending on your network or VPN.
- Units: Switch between Celsius and Fahrenheit inside the UI.

Provider-specific details & normalization
- OpenWeatherMap: icon codes are used to fetch images from OpenWeatherMap's icon endpoint.
- WeatherAPI.com: the app converts WeatherAPI responses into an OpenWeatherMap-like shape so the same UI code can display temperature, humidity, description and icons; sunrise/sunset are retrieved from WeatherAPI's forecast endpoint when available.

## Development & testing

- Add small tests and type hints when extending functionality.
- When changing requirements, update `requirements.txt` and verify the app runs locally.

## Contributing

Contributions, bug reports and feature requests are welcome. Open an issue or submit a pull request with focused changes and a short description.

## License

This project is provided for educational purposes. Check third-party API terms (OpenWeatherMap) before redistributing.

## Contact / Next steps

- To deploy to Streamlit Cloud, point the service at `SkyCast_AI/app.py` and set the `OPENWEATHER_API_KEY` in the deployment secrets.
- If using WeatherAPI in deployment, add `WEATHERAPI_KEY` to the project's secrets and choose the provider in the UI.
- If you'd like, I can also:
  - Add a minimal `.env` example and update `requirements.txt` if dependencies changed,
  - Create a short CONTRIBUTING.md and LICENSE file.