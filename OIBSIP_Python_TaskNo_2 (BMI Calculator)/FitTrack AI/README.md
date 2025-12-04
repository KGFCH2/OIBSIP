# 💪 FitTrack AI — BMI Calculator Web App 🧠⚖️  

An interactive web-based **BMI Calculator** built with **Flask (backend)** 🐍 and **vanilla JavaScript (frontend)** 💻  

---

## 🌟 Overview  

**FitTrack AI** helps users calculate their **Body Mass Index (BMI)** with a modern, responsive, and intelligent UI.  

✨ **Key Features:**  
- 🌌 Particle-animated background and polished interface  
- 📱 Responsive form with unit support *(meters / feet + inches)*  
- 🔁 Built-in **Feet + Inches → Meters** converter with precise validation  
- 🧩 Inline validation & accessible feedback messages  
- 📊 BMI legend with categories + contextual advice  
- 🌗 Light (Green)/Dark (Blue) **theme toggle**

---

## 🗂️ Project Structure  

- `frontend/` — # 🎨 Static frontend files
  - `index.html` — # 🏠 Main UI page
  - `styles.css` — # 💅 Styling, themes, responsiveness
  - `script.js` — # ⚙️ Client-side logic (validation, conversion, API)
- `server/` — # 🧠 Flask backend
  - `app.py` — # 🔌 Main Flask app (API + static serving)
  - `requirements.txt` — # 📦 Python dependencies

---

## 🚀 How to Run  

1. ✅ Ensure **Python 3.x** is installed.  
2. 📦 Install dependencies (from the `server` folder):  
   ```cmd
   cd "d:\Vs Code\PROJECT\OIBSIP\BMI Calculator\FitTrack AI\server"
   pip install -r requirements.txt
   ```

3. ▶️ Start the app (from the project folder):

Recommended (runs the server script directly):

```cmd
cd "d:\Vs Code\PROJECT\OIBSIP\BMI Calculator\FitTrack AI"
python server/app.py
```

Note: the command above runs `server/app.py` directly. The repository's `server` directory is not a Python package (no `__init__.py`), so using `python -m server.app` may fail unless you turn `server` into a package.

4. 🌐 Open your browser and visit:

```
http://127.0.0.1:5000
```

## 🧍‍♀️ Usage (Frontend)
- ⚙️ Select height units → Meters or Feet + Inches
(For feet + inches, inches field is limited to 0–11.)
- ⚖️ Enter weight (kg) — validation runs inline
- 🧮 Click Calculate to get your BMI, category, a colored category legend highlight, and tailored feedback with actionable tips.
- 🌗 You can toggle theme (Green/Blue) using the top-right button.

## 🧾 API — POST /api/bmi

Send a JSON POST to `/api/bmi` to get BMI calculations from the server. Supported input fields (provide any appropriate combination):

- 🔸 `weight_kg` (float) — weight in kilograms. Alternatively `weight_lb` (float) is accepted (server converts to kg).
- 🔸 `height_m` (float) — height in metres.
- 🔸 `height_ft` (float) and/or `height_in` (int) — feet and inches. When both are present the server will use feet+inches and convert using the exact conversion 1 inch = 0.0254 m. Decimal feet are also supported (for example `height_ft: 5.3333`).

### 📩 Example requests

#### 🧾 Metric:
```json
{ "weight_kg": 70, "height_m": 1.75 }
```

#### 👣 Feet + inches:
```json
{ "weight_kg": 70, "height_ft": 5, "height_in": 10 }
```

### 🔁 Example response
```json
{
  "bmi": 22.86,
  "category": "Normal",
  "color": "#2ECC71",
  "message": "Your BMI is 22.86 - You are in the 'Normal' category.",
  "used": "metric"  // or "ft_in" (debug/debugging field)
}
```

### 📝 Notes

- The backend uses the exact conversion 1 inch = 0.0254 m for feet+inches input to ensure accuracy.
- The `used` field is included in the response to indicate which height parsing branch was applied (helpful while debugging or testing).

## 🛠️ Development notes

- The frontend is static and served from Flask's static folder. `script.js` handles validation, UI updates, conversion and posts to `/api/bmi`.
- Accessibility: small improvements such as `aria-live` regions and labels are included so feedback is announced to assistive technologies.
- The Home page contains a BMI legend table; the matching category row is highlighted after a successful calculation.

### 💡 If you plan to extend the app:

- ➕ Add age/sex/activity inputs to provide more personalised recommendations.
- 🧪 Add unit tests that POST to `/api/bmi` and assert expected results (I can add a small test script if you want).

---
