# Nexergy AI

**Nexergy AI** is a beginner-friendly Flask web application that helps estimate electricity consumption and costs for large buildings—hospitals, software campuses, malls, colleges, hotels, offices, and more.

## Features

- Building and multi-device energy input
- kWh and billing calculations (demand/diversity factors, standby, tariff)
- Interactive dashboard with Chart.js
- Rule-based AI-style recommendations
- Solar generation and savings comparison
- Sample datasets (hospital & software company)

## Tech Stack

- Python 3 + Flask
- SQLite (`database.db`)
- Flask-SQLAlchemy
- HTML + Tailwind CSS (CDN)
- JavaScript + Chart.js

## Setup (VS Code or terminal)

1. **Open the project folder** in VS Code: `Nexergy-AI`

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

   macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:

   ```bash
   python app.py
   ```

5. Open a browser at: **http://127.0.0.1:5000**

Tables are created automatically on startup. The SQLite file `database.db` is created in the project root when you first run the app.

## Quick Start

- Visit **Home** and click **Start Energy Input**, or use **Load hospital sample** / **Load software campus sample**.
- After saving data, open **Dashboard**, **AI Tips**, and **Solar** pages.

## Project Structure

```
Nexergy-AI/
├── app.py              # Application entry point
├── config.py           # SQLite & Flask settings
├── requirements.txt
├── models/             # Database models
├── services/           # Calculations & AI rules
├── routes/             # Page blueprints
├── templates/          # HTML pages
└── static/             # CSS, JS, images
```

## Disclaimer

All calculations are **estimates** based on user-entered nameplate data and simplified formulas. They are useful for planning and education, but **not a substitute** for:

- On-site metering and load studies
- Certified energy audits
- Professional electrical engineering review
- Utility tariff and net-metering contract verification

Always validate savings and safety with qualified professionals before capital investments.

## License

Educational / demo use. Customize freely for learning projects.
