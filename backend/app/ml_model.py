"""
ML Model module for AQI prediction.
Loads trained model and makes predictions with fallback to CPCB formula.
"""

import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AQIPredictor:
    """
    Load and use ML model for AQI prediction.
    
    Features:
    - Loads trained model from disk
    - Makes predictions with proper feature engineering
    - Falls back to CPCB formula if model unavailable
    - Handles missing values gracefully
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_path = settings.model_path
        self.is_loaded = False
        self._load_model()
    
    def _load_model(self) -> bool:
        """
        Load the trained model and associated artifacts from disk.
        
        Returns:
            True if successful, False otherwise
        """
        model_dir = Path(self.model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        if not Path(self.model_path).exists():
            logger.warning(f"⚠️ No model found at {self.model_path}")
            logger.info("   Using CPCB formula fallback...")
            self.is_loaded = False
            return False
        
        try:
            # Load model
            self.model = joblib.load(self.model_path)
            logger.info(f"✅ Model loaded from {self.model_path}")
            
            # Load scaler (if exists)
            scaler_path = model_dir / "scaler.pkl"
            if scaler_path.exists():
                self.scaler = joblib.load(scaler_path)
                logger.info(f"✅ Scaler loaded from {scaler_path}")
            
            # Load feature names (if exists)
            features_path = model_dir / "feature_cols.pkl"
            if features_path.exists():
                self.feature_names = joblib.load(features_path)
                logger.info(f"✅ Feature columns loaded: {self.feature_names}")
            else:
                # Default feature order
                self.feature_names = [
                    "pm25", "pm10", "no2", "so2", "o3", "co",
                    "temperature", "humidity", "wind_speed"
                ]
                logger.info(f"ℹ️ Using default feature columns: {self.feature_names}")
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, features: Dict[str, float]) -> Optional[float]:
        """
        Predict AQI from input features.
        
        Args:
            features: Dict with keys: pm25, pm10, no2, so2, o3, co,
                     temperature, humidity, wind_speed
        
        Returns:
            Predicted AQI (0-500) or None if prediction fails
        """
        # Validate input
        if not features:
            logger.warning("Empty features provided for prediction")
            return None
        
        # If model is not loaded, use fallback
        if not self.is_loaded:
            logger.debug("Model not loaded, using fallback")
            return self._fallback_predict(features)
        
        try:
            # Prepare input data
            X = self._prepare_input(features)
            
            # Scale features if scaler is available
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
            else:
                X_scaled = X
            
            # Make prediction
            prediction = self.model.predict(X_scaled)
            
            # Round and clamp to valid AQI range (0-500)
            aqi = int(round(prediction[0]))
            aqi = max(0, min(500, aqi))
            
            logger.debug(f"✅ ML Prediction: {aqi}")
            return aqi
            
        except Exception as e:
            logger.error(f"⚠️ Prediction error: {e}")
            # Fallback to PM2.5 formula
            return self._fallback_predict(features)
    
    def _prepare_input(self, features: Dict[str, float]) -> pd.DataFrame:
        """
        Convert features dict to DataFrame for model input.
        
        Args:
            features: Dict of feature values
        
        Returns:
            DataFrame with proper feature ordering
        """
        # Get feature values in correct order
        values = []
        for feature in self.feature_names:
            value = features.get(feature)
            if value is None:
                value = 0.0  # Default to 0 for missing values
            try:
                values.append(float(value))
            except (ValueError, TypeError):
                values.append(0.0)
        
        # Return as DataFrame (1 row, N columns)
        return pd.DataFrame([values], columns=self.feature_names)
    
    def _fallback_predict(self, features: Dict[str, float]) -> Optional[float]:
        """
        Fallback prediction using CPCB formula from PM2.5.
        
        Args:
            features: Dict containing at least 'pm25' key
        
        Returns:
            AQI value or None
        """
        pm25 = features.get("pm25")
        
        if pm25 is None or pd.isna(pm25):
            logger.warning("No PM2.5 value available for fallback prediction")
            return None
        
        try:
            pm25 = float(pm25)
        except (ValueError, TypeError):
            logger.warning(f"Invalid PM2.5 value: {pm25}")
            return None
        
        aqi = self._calculate_aqi_from_pm25(pm25)
        logger.debug(f"📊 Fallback prediction from PM2.5({pm25}): AQI={aqi}")
        return aqi
    
    @staticmethod
    def _calculate_aqi_from_pm25(pm25: float) -> int:
        """
        Calculate AQI from PM2.5 using CPCB breakpoints.
        
        CPCB AQI Breakpoints for PM2.5 (µg/m³):
        - Good: 0-30 (AQI: 0-50)
        - Satisfactory: 31-60 (AQI: 51-100)
        - Moderate: 61-90 (AQI: 101-200)
        - Poor: 91-120 (AQI: 201-300)
        - Very Poor: 121-250 (AQI: 301-400)
        - Severe: 251+ (AQI: 401-500)
        """
        if pm25 <= 30:
            return int((pm25 / 30) * 50)
        elif pm25 <= 60:
            return int(50 + ((pm25 - 30) / 30) * 50)
        elif pm25 <= 90:
            return int(100 + ((pm25 - 60) / 30) * 100)
        elif pm25 <= 120:
            return int(200 + ((pm25 - 90) / 30) * 100)
        elif pm25 <= 250:
            return int(300 + ((pm25 - 120) / 130) * 100)
        else:
            return min(500, int(400 + ((pm25 - 250) / 250) * 100))
    
    def predict_batch(self, features_list: List[Dict[str, float]]) -> List[Optional[float]]:
        """
        Predict AQI for multiple feature sets.
        
        Args:
            features_list: List of feature dicts
        
        Returns:
            List of predicted AQI values
        """
        return [self.predict(features) for features in features_list]
    
    def reload_model(self) -> bool:
        """Reload the model from disk."""
        logger.info("🔄 Reloading model...")
        return self._load_model()
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dict with model metadata
        """
        info = {
            "is_loaded": self.is_loaded,
            "model_path": self.model_path,
            "feature_names": self.feature_names,
            "has_scaler": self.scaler is not None,
        }
        
        if self.is_loaded and hasattr(self.model, 'n_estimators'):
            info.update({
                "model_type": type(self.model).__name__,
                "n_estimators": getattr(self.model, 'n_estimators', 'N/A'),
                "max_depth": getattr(self.model, 'max_depth', 'N/A'),
            })
        
        return info


# ============================================
# Global Instance & Convenience Functions
# ============================================

_predictor = None


def get_predictor() -> AQIPredictor:
    """
    Get or create the global predictor instance (Singleton pattern).
    
    Returns:
        AQIPredictor instance
    """
    global _predictor
    if _predictor is None:
        _predictor = AQIPredictor()
    return _predictor


def predict_aqi(features: Dict[str, float]) -> Optional[float]:
    """
    Convenience function to predict AQI.
    
    Args:
        features: Dict with pollutant and weather values
    
    Returns:
        Predicted AQI or None
    """
    predictor = get_predictor()
    return predictor.predict(features)


def predict_aqi_batch(features_list: List[Dict[str, float]]) -> List[Optional[float]]:
    """
    Convenience function for batch predictions.
    
    Args:
        features_list: List of feature dicts
    
    Returns:
        List of predicted AQI values
    """
    predictor = get_predictor()
    return predictor.predict_batch(features_list)


def reload_model() -> bool:
    """Reload the model from disk."""
    predictor = get_predictor()
    return predictor.reload_model()


def get_model_info() -> Dict[str, Any]:
    """Get information about the loaded model."""
    predictor = get_predictor()
    return predictor.get_model_info()


# ============================================
# Quick Test Function
# ============================================

def test_predictor():
    """Test the predictor with sample data."""
    print("\n" + "=" * 50)
    print("🧪 Testing AQI Predictor")
    print("=" * 50)
    
    predictor = get_predictor()
    
    # Get model info
    info = predictor.get_model_info()
    print(f"\n📊 Model Info:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # Test with sample features
    sample_features = {
        "pm25": 150.0,
        "pm10": 200.0,
        "no2": 50.0,
        "so2": 30.0,
        "o3": 100.0,
        "co": 2.0,
        "temperature": 30.0,
        "humidity": 65.0,
        "wind_speed": 3.0,
    }
    
    print(f"\n📝 Sample Features:")
    for key, value in sample_features.items():
        print(f"   {key}: {value}")
    
    # Make prediction
    result = predictor.predict(sample_features)
    print(f"\n🎯 Predicted AQI: {result}")
    
    # Test fallback
    fallback_result = predictor._fallback_predict({"pm25": 150.0})
    print(f"📊 Fallback AQI: {fallback_result}")
    
    print("\n" + "=" * 50)
    return result


if __name__ == "__main__":
    test_predictor()