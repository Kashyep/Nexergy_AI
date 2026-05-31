"""
Solar generation and bill reduction calculations.
"""


def solar_monthly_generation_kwh(solar_kw, peak_sun_hours, days=30):
    """Solar monthly kWh = Solar kW × Peak sun hours × 30."""
    return float(solar_kw or 0) * float(peak_sun_hours or 0) * int(days)


def reduced_grid_kwh(adjusted_monthly_kwh, solar_generation_kwh):
    """Grid kWh after solar = max(Adjusted - Solar generation, 0)."""
    return max(float(adjusted_monthly_kwh or 0) - float(solar_generation_kwh or 0), 0)


def reduced_monthly_bill(reduced_kwh, tariff_rate):
    """Bill on reduced grid consumption."""
    return float(reduced_kwh or 0) * float(tariff_rate or 0)


def monthly_savings(current_bill, reduced_bill):
    """Savings = Current bill - Reduced bill."""
    return max(float(current_bill or 0) - float(reduced_bill or 0), 0)


def savings_percentage(monthly_savings, current_bill):
    """Savings % = Savings ÷ Current bill × 100."""
    bill = float(current_bill or 0)
    if bill <= 0:
        return 0.0
    return (float(monthly_savings or 0) / bill) * 100


def solar_comparison(building, adjusted_monthly_kwh, current_monthly_bill):
    """
    Complete solar simulation for templates and charts.
    """
    generation = solar_monthly_generation_kwh(building.solar_kw, building.peak_sun_hours)
    grid_kwh = reduced_grid_kwh(adjusted_monthly_kwh, generation)
    new_bill = reduced_monthly_bill(grid_kwh, building.tariff_rate)
    savings = monthly_savings(current_monthly_bill, new_bill)
    pct = savings_percentage(savings, current_monthly_bill)

    return {
        "solar_kw": building.solar_kw,
        "peak_sun_hours": building.peak_sun_hours,
        "solar_monthly_generation_kwh": round(generation, 2),
        "grid_kwh_after_solar": round(grid_kwh, 2),
        "current_monthly_bill": round(current_monthly_bill, 2),
        "reduced_monthly_bill": round(new_bill, 2),
        "monthly_savings": round(savings, 2),
        "savings_percentage": round(pct, 1),
        "annual_savings": round(savings * 12, 2),
    }
