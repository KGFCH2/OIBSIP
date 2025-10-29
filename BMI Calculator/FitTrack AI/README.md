# FitTrack AI — BMI Calculator Web App

Project: Interactive web-based BMI Calculator using Flask and vanilla JavaScript.

## Overview
This project is a web application for calculating Body Mass Index (BMI) with a modern, animated UI. It features:
- Particle animated background
- Responsive card-based interface with flip animation
- Support for multiple height/weight units
- Real-time BMI calculation and categorization
- Clean, modern design with CSS animations

## Structure
- `frontend/` — Static web frontend files
  - `index.html` — Main HTML page
  - `styles.css` — Styling and animations
  - `script.js` — Client-side JavaScript for interactions
- `server/` — Flask backend server
  - `app.py` — Main Flask application with BMI API
  - `requirements.txt` — Python dependencies

## How to Run
1. Ensure you have Python 3.x installed.
2. Install dependencies:
   ```cmd
   cd "d:\Vs Code\PROJECT\OIBSIP\BMI Calculator\FitTrack AI\server"
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```cmd
   cd "d:\Vs Code\PROJECT\OIBSIP\BMI Calculator\FitTrack AI"
   python -m server.app
   ```
4. Open your browser and go to `http://127.0.0.1:5000`

## API
The server exposes a `/api/bmi` endpoint that accepts POST requests with JSON data:
- `weight_kg`: Weight in kilograms (or `weight_lb` for pounds)
- `height_m`: Height in meters (or `height_ft` for feet, or `height_ft_int` and `height_in` for feet/inches)

Returns JSON with BMI value, category, color, and message.

## Notes
- Originally developed as a Tkinter desktop app, now converted to a web app using Flask.
- The flip animation is handled via CSS and JavaScript for smooth transitions.

License: MIT
