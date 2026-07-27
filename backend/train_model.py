"""
ML Model Training Script for AQI Prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from app.openmeteo import fetch_historical_data, calculate_aqi_from_pm25
from app.cities import get_city_coordinates


# ============================================
# CONFIGURATION
# ============================================

TRAIN_CITIES = [
    "delhi", "mumbai", "bengaluru", "chennai", 
    "hyderabad", "kolkata", "pune", "ahmedabad"
]

DAYS_BACK = 90

MODEL_PARAMS = {
    'n_estimators': 150,
    'max_depth': 15,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'n_jobs': -1
}

MODEL_PATH = "./models/aqi_model.pkl"
SCALER_PATH = "./models/scaler.pkl"
FEATURES_PATH = "./models/feature_cols.pkl"


# ============================================
# HELPER FUNCTIONS
# ============================================

def clean_column(series):
    """Convert series to float, handling None and NaN values."""
    # First convert any None to NaN
    series = series.replace([None], np.nan)
    # Then convert to float (NaN stays NaN)
    return pd.to_numeric(series, errors='coerce')


# ============================================
# FEATURE ENGINEERING
# ============================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features for AQI prediction."""
    df = df.copy()
    
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # ==========================================
    # 1. CLEAN THE DATA (FIX for NoneType error)
    # ==========================================
    # Clean weather columns
    weather_cols = ['temperature', 'humidity', 'wind_speed']
    for col in weather_cols:
        if col in df.columns:
            df[col] = clean_column(df[col])
    
    # Clean pollutant columns (if needed for AQI calculation)
    if 'pm25' in df.columns:
        df['pm25'] = clean_column(df['pm25'])
    
    # ==========================================
    # 2. TIME-BASED FEATURES
    # ==========================================
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    
    # Cyclical encoding
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    # Season (0=Winter, 1=Spring, 2=Summer, 3=Fall)
    df['season'] = df['month'].map({
        12: 0, 1: 0, 2: 0,
        3: 1, 4: 1, 5: 1,
        6: 2, 7: 2, 8: 2,
        9: 3, 10: 3, 11: 3,
    }).fillna(0).astype(int)
    
    # ==========================================
    # 3. ROLLING AVERAGES (Weather only)
    # ==========================================
    weather = ['temperature', 'humidity', 'wind_speed']
    
    for col in weather:
        if col in df.columns:
            # Ensure no NaN before rolling
            df[col] = df[col].fillna(df[col].mean())
            
            df[f'{col}_rolling_6h'] = df[col].rolling(window=6, min_periods=1).mean()
            df[f'{col}_rolling_12h'] = df[col].rolling(window=12, min_periods=1).mean()
            df[f'{col}_rolling_24h'] = df[col].rolling(window=24, min_periods=1).mean()
    
    # ==========================================
    # 4. WEATHER LAG FEATURES
    # ==========================================
    for col in weather:
        if col in df.columns:
            for lag in [1, 3, 6, 12, 24]:
                df[f'{col}_lag_{lag}h'] = df[col].shift(lag).fillna(0)
    
    # ==========================================
    # 5. WEATHER DIFFERENCES
    # ==========================================
    for col in weather:
        if col in df.columns:
            # Convert to numeric first, then diff
            df[f'{col}_diff_1h'] = df[col].diff().fillna(0)
            df[f'{col}_diff_3h'] = df[col].diff(3).fillna(0)
            df[f'{col}_diff_6h'] = df[col].diff(6).fillna(0)
    
    # ==========================================
    # 6. INTERACTION FEATURES
    # ==========================================
    if 'temperature' in df.columns and 'humidity' in df.columns:
        df['temp_humidity'] = df['temperature'] * df['humidity']
    
    if 'wind_speed' in df.columns and 'temperature' in df.columns:
        # Avoid division by zero
        df['wind_temp_ratio'] = df['wind_speed'] / (df['temperature'] + 0.1)
    
    # ==========================================
    # 7. TARGET: AQI (from PM2.5)
    # ==========================================
    if 'pm25' in df.columns:
        # Handle NaN in PM2.5 before AQI calculation
        df['pm25'] = df['pm25'].fillna(0)
        df['aqi'] = df['pm25'].apply(calculate_aqi_from_pm25)
    
    # ==========================================
    # 8. DROP ROWS WITH NaN TARGET
    # ==========================================
    df = df.dropna(subset=['aqi'])
    
    # Fill any remaining NaN values with 0
    df = df.fillna(0)
    
    return df


# ============================================
# DATA COLLECTION
# ============================================

def collect_training_data() -> pd.DataFrame:
    """Collect historical data from multiple cities."""
    print("\n" + "=" * 60)
    print("📊 COLLECTING TRAINING DATA")
    print("=" * 60)
    
    all_data = []
    
    for city in TRAIN_CITIES:
        print(f"\n📍 Fetching data for {city.upper()}...")
        
        city_info = get_city_coordinates(city)
        if not city_info:
            print(f"   ⚠️ City '{city}' not found, skipping...")
            continue
        
        df = fetch_historical_data(
            latitude=city_info['lat'],
            longitude=city_info['lon'],
            days_back=DAYS_BACK
        )
        
        if df.empty:
            print(f"   ⚠️ No data for {city}, skipping...")
            continue
        
        df['city'] = city
        df_engineered = engineer_features(df)
        
        if df_engineered.empty:
            print(f"   ⚠️ No data after feature engineering for {city}, skipping...")
            continue
        
        print(f"   ✅ Collected {len(df_engineered)} records")
        all_data.append(df_engineered)
    
    if not all_data:
        print("\n❌ No data collected.")
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n✅ Total records: {len(combined)}")
    print(f"   Cities: {combined['city'].unique().tolist()}")
    
    return combined


# ============================================
# MODEL TRAINING
# ============================================

def train_model(df: pd.DataFrame):
    """Train the Random Forest model."""
    print("\n" + "=" * 60)
    print("🤖 TRAINING MODEL")
    print("=" * 60)
    
    # ==========================================
    # 1. Define features (NO PM2.5!)
    # ==========================================
    feature_cols = [
        # Weather only (NO pollutants!)
        'temperature', 'humidity', 'wind_speed',
        # Time features
        'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos', 'season',
    ]
    
    # Weather rolling averages
    for col in ['temperature', 'humidity', 'wind_speed']:
        if col in df.columns:
            for window in [6, 12, 24]:
                feature_name = f'{col}_rolling_{window}h'
                if feature_name in df.columns:
                    feature_cols.append(feature_name)
    
    # Weather lag features
    for col in ['temperature', 'humidity', 'wind_speed']:
        if col in df.columns:
            for lag in [1, 3, 6, 12, 24]:
                feature_name = f'{col}_lag_{lag}h'
                if feature_name in df.columns:
                    feature_cols.append(feature_name)
    
    # Weather differences
    for col in ['temperature', 'humidity', 'wind_speed']:
        if col in df.columns:
            for diff in [1, 3, 6]:
                feature_name = f'{col}_diff_{diff}h'
                if feature_name in df.columns:
                    feature_cols.append(feature_name)
    
    # Interactions
    if 'temp_humidity' in df.columns:
        feature_cols.append('temp_humidity')
    if 'wind_temp_ratio' in df.columns:
        feature_cols.append('wind_temp_ratio')
    
    # Keep only existing columns
    feature_cols = [col for col in feature_cols if col in df.columns]
    
    X = df[feature_cols]
    y = df['aqi']
    
    print(f"\n📊 Features: {len(feature_cols)}")
    print(f"   Training samples: {len(X)}")
    print(f"   Target range: {y.min():.0f} - {y.max():.0f}")
    
    # ==========================================
    # 2. Split data
    # ==========================================
    split_idx = int(len(X) * 0.8)
    
    X_train = X[:split_idx]
    y_train = y[:split_idx]
    X_test = X[split_idx:]
    y_test = y[split_idx:]
    
    print(f"\n📅 Training data: {len(X_train)} samples")
    print(f"   Test data: {len(X_test)} samples")
    
    # ==========================================
    # 3. Scale features
    # ==========================================
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ==========================================
    # 4. Train model
    # ==========================================
    print("\n🚀 Training Random Forest model...")
    
    model = RandomForestRegressor(**MODEL_PARAMS)
    model.fit(X_train_scaled, y_train)
    
    # ==========================================
    # 5. Evaluate
    # ==========================================
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    train_mae = mean_absolute_error(y_train, y_pred_train)
    train_r2 = r2_score(y_train, y_pred_train)
    
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print("\n📊 MODEL PERFORMANCE:")
    print("   " + "-" * 40)
    print(f"   TRAIN SET:")
    print(f"      RMSE: {train_rmse:.2f}")
    print(f"      MAE:  {train_mae:.2f}")
    print(f"      R²:   {train_r2:.4f}")
    print(f"   TEST SET:")
    print(f"      RMSE: {test_rmse:.2f}")
    print(f"      MAE:  {test_mae:.2f}")
    print(f"      R²:   {test_r2:.4f}")
    
    # ==========================================
    # 6. Feature Importance
    # ==========================================
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n📈 TOP 15 FEATURES:")
    print("   " + "-" * 40)
    for _, row in importance.head(15).iterrows():
        print(f"   {row['feature']:30s}: {row['importance']:.4f}")
    
    # ==========================================
    # 7. Save model
    # ==========================================
    os.makedirs('./models', exist_ok=True)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(feature_cols, FEATURES_PATH)
    
    print(f"\n✅ Model saved to {MODEL_PATH}")
    print(f"✅ Scaler saved to {SCALER_PATH}")
    print(f"✅ Features saved to {FEATURES_PATH}")
    
    # ==========================================
    # 8. Save training summary
    # ==========================================
    summary = {
        'model_type': 'RandomForestRegressor',
        'train_date': datetime.now().isoformat(),
        'feature_count': len(feature_cols),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'train_rmse': train_rmse,
        'train_mae': train_mae,
        'train_r2': train_r2,
        'test_rmse': test_rmse,
        'test_mae': test_mae,
        'test_r2': test_r2,
        'top_features': importance.head(15).to_dict('records')
    }
    
    joblib.dump(summary, './models/training_summary.pkl')
    print(f"✅ Training summary saved")
    
    print("\n" + "=" * 60)
    print("🎉 MODEL TRAINING COMPLETE!")
    print("=" * 60)
    
    return model, scaler, feature_cols, summary


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Main training pipeline."""
    print("\n" + "=" * 60)
    print("🌤️  AERIQ - AQI PREDICTION MODEL TRAINING")
    print("=" * 60)
    print(f"📅 Training date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏙️  Cities: {', '.join(TRAIN_CITIES)}")
    print(f"📊 Days of data: {DAYS_BACK}")
    
    df = collect_training_data()
    
    if df.empty:
        print("\n❌ No data collected. Exiting.")
        return
    
    model, scaler, features, summary = train_model(df)
    
    print("\n🧪 VALIDATION TEST:")
    print("   Testing prediction for a sample...")
    
    sample_features = df[features].iloc[-1:].values
    sample_scaled = scaler.transform(sample_features)
    sample_pred = model.predict(sample_scaled)[0]
    sample_actual = df['aqi'].iloc[-1]
    
    print(f"   Sample Timestamp: {df['timestamp'].iloc[-1]}")
    print(f"   Actual AQI: {sample_actual:.0f}")
    print(f"   Predicted AQI: {sample_pred:.0f}")
    print(f"   Error: {abs(sample_pred - sample_actual):.0f} points")
    
    print("\n" + "=" * 60)
    print("✅ Training pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()