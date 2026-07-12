DAY 1 - The project Structure is decided

The structure has this format 


AeriQ/
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml              # GitHub Actions: run backend tests on PR
│       └── frontend-ci.yml             # GitHub Actions: run frontend build/lint on PR
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app entrypoint
│   │   ├── config.py                   # env vars, settings (Pydantic Settings)
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── aqi.py              # /api/aqi/current, /forecast, /history
│   │   │   │   ├── alerts.py           # /api/alerts/subscribe, /unsubscribe
│   │   │   │   └── health.py           # /api/health (uptime check)
│   │   │   └── deps.py                 # shared dependencies (DB session, etc.)
│   │   │
│   │   ├── models/                     # SQLAlchemy DB models
│   │   │   ├── __init__.py
│   │   │   ├── reading.py              # raw_readings table
│   │   │   ├── prediction.py           # predictions table
│   │   │   └── subscription.py         # alert_subscriptions table
│   │   │
│   │   ├── schemas/                    # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── aqi.py
│   │   │   └── alert.py
│   │   │
│   │   ├── services/                   # business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── data_fetcher.py         # calls Open-Meteo + CPCB
│   │   │   ├── prediction_service.py   # loads model, runs inference
│   │   │   └── alert_service.py        # checks thresholds, sends alerts
│   │   │
│   │   ├── alerts/
│   │   │   ├── __init__.py
│   │   │   ├── email_alert.py          # Gmail SMTP integration
│   │   │   ├── push_alert.py           # Firebase Cloud Messaging integration
│   │   │   └── scheduler.py            # APScheduler job (hourly checks)
│   │   │
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── database.py             # DB connection/session setup
│   │       └── init_db.py              # create tables, seed data
│   │
│   ├── tests/
│   │   ├── test_aqi_routes.py
│   │   ├── test_alerts.py
│   │   └── test_data_fetcher.py
│   │
│   ├── .env.example                    # documented env vars (no real secrets)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── render.yaml                     # Render deployment config
│
├── ml/
│   ├── data/
│   │   ├── raw/                        # raw pulled data (gitignored)
│   │   ├── processed/                  # cleaned/feature-engineered data (gitignored)
│   │   └── external/                   # sample/reference datasets (e.g. Kaggle practice sets)
│   │
│   ├── notebooks/
│   │   ├── 01_eda.ipynb                # exploratory data analysis
│   │   ├── 02_feature_engineering.ipynb
│   │   └── 03_model_comparison.ipynb   # RF vs XGBoost experiments
│   │
│   ├── src/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py           # fetch from Open-Meteo/CPCB, save raw data
│   │   ├── preprocessing.py            # cleaning, missing value handling
│   │   ├── feature_engineering.py      # rolling avgs, lag features, time encodings
│   │   ├── train.py                    # trains RF + XGBoost, compares, saves best
│   │   ├── evaluate.py                 # RMSE/MAE/R², SHAP feature importance
│   │   └── predict.py                  # inference function used by backend
│   │
│   ├── models/
│   │   ├── random_forest_v1.joblib     # (gitignored if large — use Git LFS or cloud storage)
│   │   └── xgboost_v1.joblib
│   │
│   ├── requirements.txt                # ML-specific deps (scikit-learn, xgboost, shap, etc.)
│   └── config.yaml                     # model hyperparameters, feature list
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api.js                  # fetch calls to backend endpoints
│   │   │   ├── stores.js               # Svelte stores (shared state)
│   │   │   └── constants.js            # AQI color bands, thresholds
│   │   │
│   │   ├── components/
│   │   │   ├── AQICard.svelte
│   │   │   ├── ForecastChart.svelte
│   │   │   ├── HistoryChart.svelte
│   │   │   ├── LocationSearch.svelte
│   │   │   ├── AlertSignupForm.svelte
│   │   │   └── AQIMap.svelte           # Leaflet.js map view
│   │   │
│   │   ├── routes/                     # pages (if using SvelteKit) or views
│   │   │   ├── +page.svelte            # dashboard home
│   │   │   └── about/+page.svelte
│   │   │
│   │   ├── App.svelte
│   │   └── main.js
│   │
│   ├── public/
│   │   └── favicon.png
│   │
│   ├── .env.example
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── vercel.json                     # Vercel deployment config
│
├── docs/
│   ├── api-contract.md                 # endpoint request/response shapes (source of truth)
│   ├── architecture-diagram.png
│   └── setup-guide.md                  # how to run the full project locally
│
├── .gitignore
├── README.md
└── LICENSE