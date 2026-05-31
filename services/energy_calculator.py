"""
Energy and billing calculation helpers for Nexergy AI.
All formulas match the project specification.
"""


def calculate_power_watts(voltage, current, power_factor):
    """Power (W) = Voltage × Current × Power Factor."""
    return float(voltage or 0) * float(current or 0) * float(power_factor or 1)


def device_daily_kwh(wattage, quantity, hours_per_day):
    """Daily kWh = Wattage × Quantity × Hours per day ÷ 1000."""
    return (float(wattage or 0) * int(quantity or 1) * float(hours_per_day or 0)) / 1000.0


def device_monthly_kwh(wattage, quantity, hours_per_day, days_per_month):
    """Monthly kWh = Daily kWh × Days per month."""
    daily = device_daily_kwh(wattage, quantity, hours_per_day)
    return daily * int(days_per_month or 30)


def standby_monthly_kwh(standby_watts, quantity, days_per_month):
    """Standby monthly kWh = Standby W × Qty × 24 × Days ÷ 1000."""
    return (
        float(standby_watts or 0) * int(quantity or 1) * 24 * int(days_per_month or 30)
    ) / 1000.0


def device_total_monthly_kwh(device):
    """Active + standby monthly energy for one device record."""
    active = device_monthly_kwh(
        device.wattage,
        device.quantity,
        device.hours_per_day,
        device.days_per_month,
    )
    standby = standby_monthly_kwh(
        device.standby_watts,
        device.quantity,
        device.days_per_month,
    )
    return active + standby


def sum_devices_monthly_kwh(devices):
    """Total monthly kWh across all devices."""
    return sum(device_total_monthly_kwh(d) for d in devices)


def adjusted_monthly_kwh(total_kwh, demand_factor, diversity_factor):
    """Adjusted kWh = Total × Demand factor × Diversity factor."""
    return float(total_kwh or 0) * float(demand_factor or 1) * float(diversity_factor or 1)


def monthly_bill(kwh, tariff_rate):
    """Monthly bill = kWh × tariff."""
    return float(kwh or 0) * float(tariff_rate or 0)


def annual_cost(monthly_bill_amount):
    """Annual cost = Monthly bill × 12."""
    return float(monthly_bill_amount or 0) * 12


def kwh_per_occupant(total_kwh, num_occupants):
    """Average monthly kWh per occupant."""
    occupants = int(num_occupants or 0)
    if occupants <= 0:
        return 0.0
    return float(total_kwh or 0) / occupants


def aggregate_by_key(devices, key_func, kwh_func=None):
    """
    Group devices by a key (name, category, block) and sum kWh.
    Returns list of {label, kwh} sorted by kwh descending.
    """
    if kwh_func is None:
        kwh_func = device_total_monthly_kwh

    totals = {}
    for device in devices:
        label = key_func(device)
        totals[label] = totals.get(label, 0) + kwh_func(device)

    result = [{"label": k, "kwh": round(v, 2)} for k, v in totals.items()]
    result.sort(key=lambda x: x["kwh"], reverse=True)
    return result


def highest_consuming_device(devices):
    """Return device with max monthly kWh, or None."""
    if not devices:
        return None, 0.0

    best = max(devices, key=device_total_monthly_kwh)
    return best, device_total_monthly_kwh(best)


def building_summary(building, devices):
    """
    Full summary dict for dashboard, solar, and recommendations.
    """
    total_kwh = sum_devices_monthly_kwh(devices)
    adjusted_kwh = adjusted_monthly_kwh(
        total_kwh, building.demand_factor, building.diversity_factor
    )
    bill = monthly_bill(adjusted_kwh, building.tariff_rate)
    annual = annual_cost(bill)
    power_w = calculate_power_watts(
        building.voltage, building.current, building.power_factor
    )

    top_device, top_kwh = highest_consuming_device(devices)

    return {
        "total_monthly_kwh": round(total_kwh, 2),
        "adjusted_monthly_kwh": round(adjusted_kwh, 2),
        "monthly_bill": round(bill, 2),
        "annual_cost": round(annual, 2),
        "power_watts": round(power_w, 2),
        "kwh_per_occupant": round(kwh_per_occupant(adjusted_kwh, building.num_occupants), 2),
        "highest_device_name": top_device.name if top_device else "N/A",
        "highest_device_kwh": round(top_kwh, 2),
        "by_device": aggregate_by_key(devices, lambda d: d.name),
        "by_category": aggregate_by_key(devices, lambda d: d.category),
        "by_block": aggregate_by_key(devices, lambda d: d.block_name or "Main"),
    }
