"""
Ideal usage benchmarks by building type (kWh per sq ft per month).
Used to compare actual consumption against typical profiles.
"""

# Approximate benchmark values for large facilities (educational estimates)
BENCHMARK_KWH_PER_SQFT = {
    "hospital": 1.8,
    "software company": 1.2,
    "mall": 1.5,
    "college": 1.1,
    "hotel": 1.4,
    "office": 1.0,
    "residential apartment": 0.6,
    "campus": 1.2,
}


def get_benchmark(building_type):
    """Return benchmark kWh/sq ft/month for a building type (case-insensitive)."""
    key = (building_type or "office").strip().lower()
    return BENCHMARK_KWH_PER_SQFT.get(key, 1.0)


def expected_monthly_kwh(building_type, building_area_sqft):
    """Ideal monthly kWh based on area and building type."""
    return get_benchmark(building_type) * float(building_area_sqft or 0)


def compare_to_benchmark(actual_kwh, building_type, building_area_sqft):
    """
    Compare actual usage to benchmark.
    Returns dict with expected, variance_pct, and status label.
    """
    expected = expected_monthly_kwh(building_type, building_area_sqft)
    if expected <= 0:
        return {"expected": 0, "variance_pct": 0, "status": "unknown"}

    variance_pct = ((actual_kwh - expected) / expected) * 100
    if variance_pct > 15:
        status = "above_benchmark"
    elif variance_pct < -15:
        status = "below_benchmark"
    else:
        status = "on_track"

    return {
        "expected": round(expected, 2),
        "variance_pct": round(variance_pct, 1),
        "status": status,
    }
