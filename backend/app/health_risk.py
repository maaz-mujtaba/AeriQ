"""
Health risk assessment engine for AeriQ.
Calculates personalized health risk scores based on:
- User health profile (age, vulnerabilities)
- City AQI
- Difference from home city
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime

from app.config import settings


# ============================================
# RISK SCORING ENGINE
# ============================================

def calculate_health_risk(
    user_profile: Dict[str, Any],
    city_aqi: int,
    home_city_aqi: int,
    city_name: str
) -> Dict[str, Any]:
    """
    Calculate personalized health risk score for a city.
    
    Args:
        user_profile: {age, vulnerabilities, city}
        city_aqi: AQI of the destination city
        home_city_aqi: AQI of the user's home city
        city_name: Name of the destination city
    
    Returns:
        Dict with risk score, category, and recommendations
    """
    age = user_profile.get("age", 30)
    vulnerabilities = user_profile.get("vulnerabilities", [])
    
    # ==========================================
    # 1. Calculate Base Risk from AQI
    # ==========================================
    aqi_risk = _calculate_aqi_risk(city_aqi)
    
    # ==========================================
    # 2. Calculate Health Factor
    # ==========================================
    health_factor = _calculate_health_factor(age, vulnerabilities)
    
    # ==========================================
    # 3. Calculate Adaptation Gap
    # ==========================================
    adaptation_gap = _calculate_adaptation_gap(city_aqi, home_city_aqi)
    
    # ==========================================
    # 4. Calculate Vulnerability Multiplier
    # ==========================================
    vuln_multiplier = _calculate_vulnerability_multiplier(vulnerabilities)
    
    # ==========================================
    # 5. Calculate Final Risk Score (0-100)
    # ==========================================
    raw_risk = (
        aqi_risk * 
        health_factor * 
        (1 + adaptation_gap) * 
        vuln_multiplier
    )
    
    risk_score = min(100, max(0, raw_risk))
    
    # ==========================================
    # 6. Determine Risk Category
    # ==========================================
    risk_category, risk_color = _get_risk_category(risk_score)
    
    # ==========================================
    # 7. Generate Recommendations
    # ==========================================
    recommendations = _generate_recommendations(
        risk_score, risk_category, vulnerabilities, city_aqi, home_city_aqi
    )
    
    return {
        "risk_score": round(risk_score, 1),
        "risk_category": risk_category,
        "risk_color": risk_color,
        "aqi_risk": round(aqi_risk, 1),
        "health_factor": round(health_factor, 2),
        "adaptation_gap": round(adaptation_gap, 2),
        "vulnerability_multiplier": round(vuln_multiplier, 2),
        "recommendations": recommendations,
        "is_riskier_than_home": city_aqi > home_city_aqi
    }


def _calculate_aqi_risk(aqi: int) -> float:
    """Calculate base risk from AQI value."""
    if aqi <= 50:
        return 10.0  # Good
    elif aqi <= 100:
        return 25.0  # Satisfactory
    elif aqi <= 200:
        return 50.0  # Moderate
    elif aqi <= 300:
        return 75.0  # Poor
    elif aqi <= 400:
        return 90.0  # Very Poor
    else:
        return 100.0  # Severe


def _calculate_health_factor(age: int, vulnerabilities: List[str]) -> float:
    """Calculate health factor based on age and vulnerabilities."""
    # Age factor
    if age < 5:
        age_factor = 2.5  # Children very vulnerable
    elif age < 18:
        age_factor = 1.2
    elif age < 40:
        age_factor = 1.0
    elif age < 60:
        age_factor = 1.5
    elif age < 75:
        age_factor = 2.0
    else:
        age_factor = 2.5  # Elderly
    
    # Vulnerability factor
    if vulnerabilities and vulnerabilities != ["none"]:
        vuln_factor = 1.5
    else:
        vuln_factor = 1.0
    
    # Combined health factor
    return age_factor * vuln_factor


def _calculate_adaptation_gap(city_aqi: int, home_aqi: int) -> float:
    """Calculate adaptation gap between home and destination."""
    if home_aqi == 0:
        home_aqi = 1
    
    if city_aqi <= home_aqi:
        return 0.0  # No gap if destination is cleaner
    
    gap = (city_aqi - home_aqi) / home_aqi
    return min(1.0, gap)  # Cap at 1.0


def _calculate_vulnerability_multiplier(vulnerabilities: List[str]) -> float:
    """Calculate multiplier based on specific vulnerabilities."""
    multiplier = 1.0
    
    # Weight by severity
    severity_map = {
        "asthma": 2.0,
        "respiratory": 1.8,
        "heart_disease": 1.6,
        "elderly": 1.5,
        "child": 1.8,
        "general": 1.0,
        "none": 1.0
    }
    
    for vuln in vulnerabilities:
        if vuln in severity_map:
            multiplier = max(multiplier, severity_map[vuln])
    
    return multiplier


def _get_risk_category(score: float) -> Tuple[str, str]:
    """Get risk category and color based on score."""
    if score < 25:
        return "Safe", "#00FF00"
    elif score < 50:
        return "Caution", "#FFA500"
    elif score < 75:
        return "High Risk", "#FF0000"
    else:
        return "Avoid", "#8B0000"


def _generate_recommendations(
    risk_score: float,
    risk_category: str,
    vulnerabilities: List[str],
    city_aqi: int,
    home_aqi: int
) -> Dict[str, List[str]]:
    """Generate personalized recommendations."""
    recs = {
        "general": [],
        "medical": [],
        "travel": [],
        "emergency": []
    }
    
    # Risk level recommendations
    if risk_category == "Safe":
        recs["general"].append("Normal precautions recommended")
    elif risk_category == "Caution":
        recs["general"].append("Limit outdoor activities during peak pollution hours (6-10 AM, 5-8 PM)")
        recs["travel"].append("Consider using N95 masks when outdoors")
    elif risk_category == "High Risk":
        recs["general"].append("AVOID outdoor activities")
        recs["medical"].append("Keep emergency medication accessible at all times")
        recs["travel"].append("Book accommodations with air purifiers")
        recs["emergency"].append("Identify nearest hospital with specialist")
    else:  # Avoid
        recs["general"].append("STRONGLY RECOMMENDED: Reschedule travel")
        recs["medical"].append("Consult your doctor before traveling")
        recs["emergency"].append("Emergency protocol required")
    
    # Vulnerability-specific
    if "asthma" in vulnerabilities:
        recs["medical"].extend([
            "Carry 2x extra inhalers/medication",
            "Monitor breathing hourly",
            "Avoid morning outdoor activities"
        ])
    
    if "heart_disease" in vulnerabilities:
        recs["medical"].extend([
            "Monitor heart rate regularly",
            "Avoid strenuous activities",
            "Stay hydrated"
        ])
    
    if "elderly" in vulnerabilities or "child" in vulnerabilities:
        recs["general"].extend([
            "Keep indoors as much as possible",
            "Use air purifiers in closed rooms",
            "Maintain proper ventilation"
        ])
    
    # AQI-specific
    if city_aqi > 200:
        recs["travel"].append("Stay indoors with windows closed")
        recs["medical"].append("Use saline nasal spray to clear particles")
    
    if city_aqi > 100 and home_aqi < 100:
        recs["travel"].append("Gradually acclimate to new environment")
    
    # Remove duplicates
    for key in recs:
        recs[key] = list(set(recs[key]))
    
    return recs


def get_default_threshold(vulnerabilities: List[str]) -> int:
    """Get default alert threshold based on vulnerabilities."""
    if not vulnerabilities or vulnerabilities == ["none"]:
        return settings.alert_thresholds.get("general", 100)
    
    # Use the most restrictive threshold
    thresholds = []
    for vuln in vulnerabilities:
        if vuln in settings.alert_thresholds:
            thresholds.append(settings.alert_thresholds[vuln])
    
    if thresholds:
        return min(thresholds)  # Use the most restrictive (lowest) threshold
    
    return settings.alert_thresholds.get("general", 100)