# FitTrack AI — Interactive GUI BMI Calculator (Tkinter)

Project: Interactive GUI BMI Calculator using Python Tkinter.

Overview
--------
This project demonstrates an intermediate-level desktop GUI built with Python 3 and Tkinter. It includes:
- A particle animated background
- Dark/Light theme toggle with persistence
- A card container that simulates a flip to reveal results
- Input validation and helpful alerts
- Hover/glow effects and a soft click sound on Windows

Structure
---------
- `backend/` — Python application and tests
  - `app.py` — Main Tkinter GUI application
  - `bmi.py` — BMI calculation and categorization logic (tested)
  - `test_bmi.py` — pytest unit tests for the logic
  - `requirements.txt` — test/runtime requirements
- `frontend/` — placeholder for assets (icons, sounds). See `ASSETS_README.txt`.

How to run
----------
1. Ensure you have Python 3.x installed and available on PATH.
2. (Optional) Create a virtual environment and activate it.
3. Install test dependencies if you want to run tests:

```cmd
cd "d:\\Vs Code\\PROJECT\\OIBSIP\\BMI Calculator\\FitTrack AI\\backend"
python -m pip install -r requirements.txt
```

4. Run the app:

```cmd
cd "d:\\Vs Code\\PROJECT\\OIBSIP\\BMI Calculator\\FitTrack AI"
python -m backend.app
```

5. Run tests:

```cmd
cd "d:\\Vs Code\\PROJECT\\OIBSIP\\BMI Calculator\\FitTrack AI"
python -m pytest -q
```

Notes & Extensions
------------------
- The flip animation is simulated by shrinking/expanding the card window width and swapping the front/back content. This keeps the solution simple and cross-platform with Tkinter.
- To add an app icon or sounds, place them in `frontend/` and update `backend/app.py` accordingly.
- For more advanced visuals consider integrating Pillow for image effects or using an embedded browser (webview) for CSS/JS-powered UIs.

License: MIT (adapt as you prefer)
