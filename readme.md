<div align="center">

# AeriQ

### Air Quality Prediction & Health Risk Assessment System

An end-to-end ML-powered platform that forecasts AQI for **277 Indian cities** and translates pollution data into **personalized health risk scores** for vulnerable populations.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte-4.0+-FF3E00?style=flat&logo=svelte&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#️-architecture)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Technology Stack](#️-technology-stack)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#️-database-schema)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Design Decisions & Trade-offs](#-design-decisions--trade-offs)
- [Future Work](#-future-work)
- [References](#-references)
- [License](#-license)
- [Team](#-team)

---

## 📌 Overview

Air pollution causes **2+ million premature deaths annually in India**, with asthma patients, the elderly, and individuals with respiratory conditions being disproportionately affected. Existing air quality platforms surface raw AQI numbers but leave users to interpret what those numbers mean for their health.

**AeriQ bridges that gap.** It combines:

1. **AQI Prediction** — A Random Forest regressor trained on 90 days of historical data from 8 Indian cities, achieving **R² = 0.9612** (96% variance explained) and **MAE = 1.77** on held-out test data.

2. **Personalized Health Risk Assessment** — A rule-based engine that computes a **0–100 risk score** from a user's age, health vulnerabilities, and home-vs-destination AQI, then generates actionable medical and travel recommendations.

The system serves 277 Indian cities through a **FastAPI backend with 14+ REST endpoints**, JWT authentication, and PostgreSQL persistence, paired with a **Svelte frontend** for real-time visualization.

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| **AQI Prediction** | Random Forest model predicting AQI 24–72 hours ahead with 96% accuracy |
| **Personalized Risk Score** | 0–100 health risk score based on age, vulnerabilities, and home city baseline |
| **City Comparison** | Side-by-side AQI comparison with adaptation gap analysis for travelers |
| **277 Indian Cities** | Comprehensive city database with lat/lon coordinates |
| **JWT Authentication** | Secure registration, login, and profile management |
| **Actionable Recommendations** | Medication planning, emergency protocols, and travel safety advice |
| **Graceful Degradation** | CPCB formula fallback when ML model or external API is unavailable |
| **Swagger/OpenAPI** | Auto-generated interactive API documentation |

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AERIQ SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐      ┌─────────────────┐      ┌──────────────────────┐   │
│   │   Frontend  │─────▶│  FastAPI Backend │─────▶│   Open-Meteo API     │   │
│   │   (Svelte)  │◀─────│   (Python)       │◀─────│   (Real-time Data)   │   │
│   └─────────────┘      └────────┬─────────┘      └──────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────────┐                          │
│                    │   ML Inference Layer        │                          │
│                    │   (Random Forest Regressor) │                          │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   Health Risk Engine        │                          │
│                    │   (Rule-based scoring)      │                          │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │   PostgreSQL Database       │                          │
│                    │   (User data persistence)   │                          │
│                    └─────────────────────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Design principles:**

- **Separation of concerns** — Frontend communicates exclusively through the FastAPI contract; ML models and the risk engine are fully decoupled from the UI.
- **Graceful degradation** — If the ML model is unavailable, the backend falls back to a deterministic CPCB formula.
- **Stateless authentication** — JWT tokens enable horizontal scaling without session storage.
- **Database abstraction** — SQLAlchemy ORM allows swapping SQLite (dev) for PostgreSQL (prod) without code changes.

---

## 🤖 Machine Learning Pipeline

### Data Collection

- **Source:** [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api) (free, no key required)
- **Coverage:** 8 Indian cities — Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Kolkata, Pune, Ahmedabad
- **Volume:** 90 days of hourly data per city (~17,472 total records)
- **Features:** PM2.5, PM10, NO2, SO2, O3, CO, temperature, humidity, wind speed

### Feature Engineering (70+ features)

| Category | Features | Purpose |
|---|---|---|
| **Time** | `hour_sin/cos`, `dow_sin/cos`, `season` | Capture daily, weekly, and seasonal patterns |
| **Lagged** | `pm25_lag_{1,3,6,12,24}h` | Use past pollution to predict future AQI |
| **Rolling** | `pm25_rolling_{6,12,24}h` | Smooth noise, capture trends |
| **Difference** | `pm25_diff_{1,3,6}h` | Rate of change matters |
| **Interaction** | `temp_humidity`, `wind_pm25_ratio` | Weather-pollutant interactions |

### Data Leakage Prevention

> AQI is calculated from PM2.5. Using *current* PM2.5 as a feature would let the model learn the AQI formula instead of predicting it. We **removed current PM2.5** and used only lagged values — forcing the model to learn temporal patterns.

### Model Configuration

```python
RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1
)
```

### Performance Metrics

| Metric | Train | Test | Interpretation |
|---|---|---|---|
| **R²** | 0.9938 | 0.9612 | Explains 96% of AQI variance |
| **RMSE** | 5.88 | 2.94 | Penalizes large errors |
| **MAE** | 1.91 | 1.77 | Predicts within ~2 AQI points |

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic |
| **ML** | scikit-learn, XGBoost, Pandas, NumPy, joblib |
| **Database** | PostgreSQL (production), SQLite (development), Supabase |
| **Frontend** | Svelte, Vite, Tailwind CSS, Chart.js, Leaflet.js |
| **Auth** | JWT (python-jose), passlib (sha256_crypt) |
| **Data Source** | Open-Meteo Air Quality API |
| **Deployment** | Render (backend), Vercel (frontend), Supabase (DB) |
| **Testing** | pytest, httpx |
| **CI/CD** | GitHub Actions |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+ (or SQLite for development)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/AeriQ.git
cd AeriQ/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and secret key

# Initialize database
python init_db.py

# Train the ML model (first time only)
python train_model.py

# Run the server
uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**.
Interactive documentation: **http://localhost:8000/docs**

### Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

The frontend will be available at **http://localhost:5173**.

### Docker

```bash
docker build -t aeriq-backend ./backend
docker run -p 8000:8000 --env-file ./backend/.env aeriq-backend
```

---

## 📡 API Endpoints

### Public (No Auth Required)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Authenticate and receive JWT |
| `POST` | `/api/predict` | Predict AQI for a city |
| `GET` | `/api/predict/{city}` | Predict AQI (GET variant) |
| `GET` | `/api/cities` | List or search 277 cities |
| `GET` | `/api/city-count` | Total cities available |

### Protected (JWT Required)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/auth/me` | Get current user profile |
| `PUT` | `/api/auth/me` | Update user profile |
| `POST` | `/api/health/assess` | Personalized health risk assessment |
| `GET` | `/api/health/my-threshold` | Get user's alert threshold |
| `GET` | `/api/compare/{city1}/{city2}` | Compare AQI between two cities |

### Example Response

```json
{
  "city": "Delhi",
  "state": "Delhi",
  "latitude": 28.6139,
  "longitude": 77.209,
  "aqi": 340,
  "aqi_category": "Severe",
  "aqi_color": "#8B0000",
  "pm25": 280.5,
  "pm10": 420.3,
  "prediction_source": "ml_model"
}
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    age             INTEGER,
    gender          VARCHAR(20),
    city            VARCHAR(100),
    vulnerabilities TEXT DEFAULT '[]',  -- JSON array
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);
```

> **Design note:** Only user data is persisted. AQI readings and predictions are fetched/generated on-the-fly, eliminating stale data and reducing storage costs.

---

## 🧪 Testing

```bash
# Run backend tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

---

## 📁 Project Structure

```text
AeriQ/
├── .github/
│   └── workflows/              # CI pipelines (backend + frontend)
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint
│   │   ├── config.py           # Pydantic settings
│   │   ├── database.py         # SQLAlchemy engine/session
│   │   ├── db_models.py        # ORM models
│   │   ├── models.py           # Pydantic schemas
│   │   ├── auth.py             # JWT + password hashing
│   │   ├── crud.py             # DB operations
│   │   ├── cities.py           # 277-city loader
│   │   ├── openmeteo.py        # External API client
│   │   ├── ml_model.py         # Model loading + inference
│   │   ├── health_risk.py      # Risk scoring engine
│   │   └── routes.py           # API endpoints
│   ├── data/
│   │   └── city_coordinates.csv
│   ├── models/                 # Trained model artifacts
│   ├── tests/
│   ├── train_model.py          # ML training script
│   ├── init_db.py              # DB initialization
│   ├── requirements.txt
│   ├── Dockerfile
│   └── render.yaml
├── frontend/
│   ├── src/
│   │   ├── lib/                # API client, stores, components
│   │   └── routes/             # SvelteKit pages
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docs/
│   ├── api-contract.md
│   ├── architecture-diagram.png
│   └── setup-guide.md
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🎯 Design Decisions & Trade-offs

| Decision | Rationale |
|---|---|
| **Random Forest over Neural Networks** | Tabular data, limited training samples (~17k), need for feature importance, and interpretability for health-critical applications |
| **Remove current PM2.5** | Prevents data leakage; forces temporal learning |
| **Rule-based health risk engine** | ML for AQI is appropriate; health risk requires transparent, auditable logic for medical recommendations |
| **SQLAlchemy ORM** | Database-agnostic; enables SQLite → PostgreSQL migration without code changes |
| **JWT over session cookies** | Stateless authentication; horizontally scalable |
| **CPCB fallback** | Graceful degradation when ML model or external API is unavailable |

---

## 🔮 Future Work

- [ ] **Alert system** — Email (Gmail SMTP) and push notifications (Firebase FCM) when AQI crosses personalized thresholds
- [ ] **XGBoost comparison** — Evaluate gradient boosting against Random Forest for potential accuracy gains
- [ ] **Model retraining pipeline** — Scheduled retraining with new data to combat drift
- [ ] **SHAP explainability** — Per-prediction feature attributions for transparency
- [ ] **Mobile app** — React Native client for on-the-go access
- [ ] **Global expansion** — Extend beyond Indian cities using Open-Meteo's global coverage

---

## 📚 References

1. Open-Meteo, "Air Quality API Documentation," *Open-Meteo*. [Online]. Available: https://open-meteo.com/en/docs/air-quality-api
2. Central Pollution Control Board, "National Air Quality Index," *CPCB*. [Online]. Available: https://cpcb.nic.in/National-Air-Quality-Index
3. L. Breiman, "Random Forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
4. T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Min.*, 2016, pp. 785–794.
5. FastAPI, "FastAPI Documentation," *FastAPI*. [Online]. Available: https://fastapi.tiangolo.com
6. Svelte, "Svelte Documentation," *Svelte*. [Online]. Available: https://svelte.dev/docs
7. Supabase, "Supabase Documentation," *Supabase*. [Online]. Available: https://supabase.com/docs

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Team ID:** CS_AI_3A_05
**Course:** BCS-554 Mini Project

| Role | Name |
|---|---|
| Backend + ML Lead | [Name] |
| Backend Support | [Name] |
| Backend Support | [Name] |
| Frontend Lead | [Name] |
| Frontend Support | [Name] |

---

<p align="center">
  <i>Built with a focus on clean architecture, measurable ML performance, and real-world health impact.</i>
</p>
