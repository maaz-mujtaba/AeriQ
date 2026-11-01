<div align="center">

# AeriQ

**Air Quality Forecasting & Personalized Health Risk Assessment for India**

An ML-powered platform that predicts AQI for 277 Indian cities and turns pollution data into personalized health risk scores for vulnerable populations.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)
![SvelteKit](https://img.shields.io/badge/SvelteKit-FF3E00?style=flat&logo=svelte&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

> **Medical disclaimer:** AeriQ provides general information and is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified clinician about your health.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Engineering Challenges](#engineering-challenges)
- [Design Decisions & Trade-offs](#design-decisions--trade-offs)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [References](#references)
- [License](#license)
- [Team](#team)

---

## Overview

Air pollution is a leading public-health burden in India, with an estimated 1.67 million attributable deaths in 2019 [[1]](#references). Asthma patients, the elderly, and people with respiratory or cardiac conditions are disproportionately affected. Most air-quality platforms show a raw AQI number and leave users to work out what it means for them.

AeriQ closes that gap with two components:

1. **AQI forecasting.** A Random Forest regressor trained on hourly Open-Meteo data from 8 Indian cities.
2. **Personalized health risk assessment.** A transparent, rule-based engine that computes a 0â€“100 risk score from a user's age, health vulnerabilities, and home-vs-destination AQI, then generates medication-planning and travel recommendations.

Everything is served through a FastAPI backend (JWT auth, PostgreSQL persistence) and a SvelteKit frontend.

---

## Key Features

| Feature | Description |
|---|---|
| **AQI Prediction** | Random Forest forecast of AQI from lagged pollutant and weather features |
| **Personalized Risk Score** | 0â€“100 score based on age, vulnerabilities, and home-city baseline |
| **City Comparison** | Side-by-side AQI comparison with an adaptation-gap analysis for travelers |
| **277 Indian Cities** | City database with latitude/longitude coordinates |
| **JWT Authentication** | Registration, login, and profile management |
| **Actionable Recommendations** | Medication planning, emergency protocols, and travel safety advice |
| **Graceful Degradation** | Falls back to a deterministic CPCB sub-index formula if the ML model or external API is unavailable |
| **OpenAPI Docs** | Interactive Swagger UI at `/docs` |

---

## Architecture

```text
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Frontend   â”‚â”€â”€â”€â”€â–¶â”‚  FastAPI Backend  â”‚â”€â”€â”€â”€â–¶â”‚  Open-Meteo API    â”‚
â”‚  (SvelteKit) â”‚â—€â”€â”€â”€â”€â”‚     (Python)      â”‚â—€â”€â”€â”€â”€â”‚  (air quality)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                               â”‚
              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
              â–¼                â–¼                 â–¼
     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â”‚  ML Inference  â”‚ â”‚ Health Risk  â”‚ â”‚  PostgreSQL   â”‚
     â”‚ (Random Forest)â”‚ â”‚ Engine (rules)â”‚ â”‚ (user data)   â”‚
     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Design principles**

- **Separation of concerns:** the frontend talks only to the FastAPI contract; the ML model and risk engine are decoupled from the UI.
- **Graceful degradation:** a CPCB formula fallback keeps the service responsive when the model or upstream API fails.
- **Stateless auth:** JWT tokens avoid server-side session storage.
- **Database abstraction:** SQLAlchemy lets development use SQLite and production use PostgreSQL without code changes.

---

## Machine Learning Pipeline

### Data

| Item | Detail |
|---|---|
| Source | [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) (free, no key) |
| Cities | Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad |
| Volume | 90 days of hourly data per city (8 Ã— 90 Ã— 24 = **17,280** records) |
| Variables | PM2.5, PM10, NOâ‚‚, SOâ‚‚, Oâ‚ƒ, CO, temperature, humidity, wind speed |

> Open-Meteo values come from an atmospheric model (CAMS), not ground sensors. They are smoother and more predictable than station readings, so accuracy here should not be assumed to transfer to real monitors.

### Feature Engineering

| Category | Features | Purpose |
|---|---|---|
| Time | `hour_sin/cos`, `dow_sin/cos`, `season` | Daily, weekly, and seasonal cycles |
| Lagged | `pm25_lag_{1,3,6,12,24}h` | Past pollution as a predictor |
| Rolling | `pm25_rolling_{6,12,24}h` (past-only windows) | Trend and noise smoothing |
| Difference | `pm25_diff_{1,3,6}h` | Rate of change |
| Interaction | `temp_humidity`, `wind_pm25_ratio` | Weatherâ€“pollutant effects |

### Leakage Prevention

AQI is derived from pollutant concentrations (PM2.5, PM10, and others), so any feature that exposes the *current* value lets the model reproduce the formula instead of forecasting.

- Features use only information available at prediction time `t`; the target is AQI at `t + h`.
- Current-hour PM2.5 is excluded. Rolling windows are computed on past values only.
- Because `lag + diff` can reconstruct the current value, differences are computed between lagged values (e.g. `lag_1 âˆ’ lag_2`), never against the current hour.
- Current-hour PM10, NOâ‚‚, SOâ‚‚, Oâ‚ƒ, and CO are treated the same way, since AQI is the maximum of per-pollutant sub-indices.

### Model

```python
RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1,
)
```

### Evaluation Status

The checked-in training run evaluates a single-step AQI estimate, not forecasts at 1, 24, 48, or 72 hours. It uses a chronological 80/20 row split after concatenating city data; it does not implement the per-city time split, persistence baseline, CPCB baseline, or held-out-city test described in the earlier draft of this section. Those multi-horizon results have not been measured, so they are not reported here.

### Results

| Saved run (2026-10-21) | Test MAE | Test RMSE | Test R-squared |
|---|---:|---:|---:|
| Single-step AQI estimate | 2.45 | 4.79 | 0.9704 |

These values are from `backend/models/training_summary.pkl` (13,977 training rows; 3,495 test rows; 70 features). Treat them as a legacy benchmark, not as evidence of future-horizon or cross-city forecasting performance. The training script and evaluation protocol need to be updated before those claims can be reported.
---

## Technology Stack

| Layer | Technologies |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic |
| ML | scikit-learn, Pandas, NumPy, joblib |
| Database | PostgreSQL (production), SQLite (development), Supabase |
| Frontend | SvelteKit, Vite, Tailwind CSS, Chart.js, Leaflet.js |
| Auth | JWT (python-jose), passlib (bcrypt) |
| Data source | Open-Meteo Air Quality API |
| Deployment | Render (backend), Vercel (frontend), Supabase (DB) |
| Testing / CI | pytest, httpx, GitHub Actions |

---

## Getting Started

### Prerequisites

- Python 3.10+ (3.11 recommended)
- Node.js 18+
- PostgreSQL 15+ (or SQLite for development)

### Backend

```bash
git clone https://github.com/<your-username>/AeriQ.git
cd AeriQ/backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # set DATABASE_URL and SECRET_KEY

python init_db.py               # initialize the database
python train_model.py           # train the model (first run only)

uvicorn app.main:app --reload
```

API: <http://localhost:8000> Â· Docs: <http://localhost:8000/docs>

### Frontend

```bash
cd ../frontend
npm install
npm run dev
```

Frontend: <http://localhost:5173>

### Docker

```bash
docker build -t aeriq-backend ./backend
docker run -p 8000:8000 --env-file ./backend/.env aeriq-backend
```

---

## API Endpoints

### Public

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate and receive a JWT |
| POST | `/api/predict` | Predict AQI for a city |
| GET | `/api/predict/{city}` | Predict AQI (GET variant) |
| GET | `/api/cities` | List or search cities |
| GET | `/api/city-count` | Total cities available |

### Protected (JWT required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/auth/me` | Get current user profile |
| PUT | `/api/auth/me` | Update user profile |
| POST | `/api/health/assess` | Personalized health risk assessment |
| GET | `/api/health/my-threshold` | Get the user's alert threshold |
| GET | `/api/compare/{city1}/{city2}` | Compare AQI between two cities |

### Example Response

```json
{
  "city": "Delhi",
  "state": "Delhi",
  "latitude": 28.6139,
  "longitude": 77.209,
  "aqi": 340,
  "aqi_category": "Very Poor",
  "aqi_color": "#FF0000",
  "pm25": 280.5,
  "pm10": 420.3,
  "prediction_source": "ml_model"
}
```

`prediction_source` is `ml_model` or `cpcb_fallback`, so clients can tell which path produced the value.

CPCB categories: Good (0â€“50), Satisfactory (51â€“100), Moderate (101â€“200), Poor (201â€“300), Very Poor (301â€“400), Severe (401â€“500).

---

## Database Schema

```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    age             INTEGER,
    gender          VARCHAR(20),
    city            VARCHAR(100),
    vulnerabilities TEXT DEFAULT '[]',   -- JSON array
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);
```

Only user data is persisted. AQI readings and predictions are fetched or generated on demand, which avoids stale data and keeps storage small. Health and profile data is sensitive: keep it out of logs and use HTTPS in production.

---

## Testing

```bash
pytest tests/ -v
pytest --cov=app tests/
```

Current status: _add test count and coverage % here_.

---

## Project Structure

```text
AeriQ/
â”œâ”€â”€ .github/workflows/        # CI pipelines (backend + frontend)
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ main.py           # FastAPI entrypoint
â”‚   â”‚   â”œâ”€â”€ config.py         # Pydantic settings
â”‚   â”‚   â”œâ”€â”€ database.py       # SQLAlchemy engine/session
â”‚   â”‚   â”œâ”€â”€ db_models.py      # ORM models
â”‚   â”‚   â”œâ”€â”€ models.py         # Pydantic schemas
â”‚   â”‚   â”œâ”€â”€ auth.py           # JWT + password hashing
â”‚   â”‚   â”œâ”€â”€ crud.py           # DB operations
â”‚   â”‚   â”œâ”€â”€ cities.py         # City loader
â”‚   â”‚   â”œâ”€â”€ openmeteo.py      # External API client
â”‚   â”‚   â”œâ”€â”€ ml_model.py       # Model loading + inference
â”‚   â”‚   â”œâ”€â”€ health_risk.py    # Risk scoring engine
â”‚   â”‚   â””â”€â”€ routes.py         # API endpoints
â”‚   â”œâ”€â”€ alembic/              # Database migrations
â”‚   â”œâ”€â”€ data/city_coordinates.csv
â”‚   â”œâ”€â”€ models/               # Trained model artifacts
â”‚   â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ train_model.py
â”‚   â”œâ”€â”€ init_db.py
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â”œâ”€â”€ Dockerfile
â”‚   â””â”€â”€ render.yaml
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ lib/              # API client, stores, components
â”‚   â”‚   â””â”€â”€ routes/           # SvelteKit pages
â”‚   â”œâ”€â”€ package.json
â”‚   â”œâ”€â”€ tailwind.config.js
â”‚   â””â”€â”€ vite.config.js
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ api-contract.md
â”‚   â”œâ”€â”€ architecture-diagram.png
â”‚   â””â”€â”€ setup-guide.md
â”œâ”€â”€ LICENSE
â””â”€â”€ README.md
```

---

## Engineering Challenges

- **Data leakage in time-series ML.** AQI is computed from pollutant concentrations, so including current-hour values, or lag/difference combinations that reconstruct them, lets the model recover the formula instead of forecasting. Fixing this meant redefining features relative to the prediction time and switching to chronological evaluation with a persistence baseline.
- **Cloud deployment.** Moving from local to hosted exposed IPv4/IPv6 connectivity problems (switching from Supabase's direct connection to the shared session pooler for Render), Python version conflicts (pinning 3.11 so pre-built pandas wheels were used), and CORS configuration between the Vercel frontend and the Render backend.

---

## Design Decisions & Trade-offs

| Decision | Rationale |
|---|---|
| Random Forest over neural networks | Small tabular dataset, built-in feature importance, easier to interpret |
| Rule-based health risk engine | Medical recommendations need transparent, auditable logic; ML is used only where it adds value (AQI forecasting) |
| Exclude current-hour pollutant values | Prevents the model from learning the AQI formula |
| SQLAlchemy ORM | SQLite for dev, PostgreSQL for prod, no code changes |
| JWT over session cookies | Stateless and horizontally scalable |
| CPCB fallback | Keeps the service available when the model or upstream API fails |

---

## Limitations

- The model is trained on **8 cities** but the app serves **277**. Predictions for other cities are extrapolations; validate with the held-out-city test above.
- Training data is **modeled (CAMS) data from 90 days**, so it does not cover a full annual cycle (e.g. Delhi's winter stubble-burning peak).
- The health risk score is a heuristic, not a clinically validated instrument.

---

## Future Work

- [ ] Alerts: email (SMTP) and push (Firebase FCM) when AQI crosses a personal threshold
- [ ] XGBoost vs. Random Forest comparison
- [ ] Scheduled retraining to handle drift, with 12+ months of data
- [ ] SHAP explanations for individual predictions
- [ ] Validation against CPCB ground-station data
- [ ] Mobile client (React Native)
- [ ] Coverage beyond India using Open-Meteo's global data

---

## References


1. Open-Meteo, "Air Quality API Documentation." <https://open-meteo.com/en/docs/air-quality-api>
2. Central Pollution Control Board, "National Air Quality Index." <https://cpcb.nic.in/National-Air-Quality-Index>
3. L. Breiman, "Random Forests," *Machine Learning*, vol. 45, no. 1, pp. 5â€“32, 2001.
4. FastAPI Documentation. <https://fastapi.tiangolo.com>
5. Svelte Documentation. <https://svelte.dev/docs>
6. Supabase Documentation. <https://supabase.com/docs>

---



<p align="center"><i>Built with a focus on clean architecture, honest evaluation, and real-world health impact.</i></p>
