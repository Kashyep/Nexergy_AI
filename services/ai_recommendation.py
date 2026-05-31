"""
Rule-based AI-style energy recommendations.
Each item includes title, message, estimated savings, priority, and energy impact.
"""
from services.energy_calculator import device_total_monthly_kwh, sum_devices_monthly_kwh
from services.solar_calculator import solar_monthly_generation_kwh, monthly_savings, reduced_monthly_bill
from services.solar_calculator import reduced_grid_kwh
from services.benchmark_data import compare_to_benchmark


def _rec(title, message, savings, priority="Medium", impact="Medium"):
    return {
        "title": title,
        "message": message,
        "estimated_savings": round(float(savings or 0), 2),
        "priority": priority,
        "energy_impact": impact,
    }


def generate_recommendations(building, devices, summary, solar_summary=None):
    """
    Analyze devices and building data; return list of recommendation dicts.
    """
    recommendations = []
    tariff = float(building.tariff_rate or 0)
    total_kwh = summary.get("adjusted_monthly_kwh", 0)
    monthly_bill = summary.get("monthly_bill", 0)

    if not devices:
        recommendations.append(
            _rec(
                "Add device data",
                "No devices recorded yet. Add HVAC, lighting, and IT loads for accurate insights.",
                0,
                "High",
                "High",
            )
        )
        return recommendations

    # Category totals
    hvac_cats = {"hvac", "air conditioner", "chiller", "ahu", "fan"}
    by_cat = {}
    for d in devices:
        cat = (d.category or "other").lower()
        by_cat[cat] = by_cat.get(cat, 0) + device_total_monthly_kwh(d)

    total_device_kwh = sum(by_cat.values()) or 1

    # High HVAC usage
    hvac_kwh = sum(by_cat.get(c, 0) for c in hvac_cats)
    if hvac_kwh / total_device_kwh > 0.35:
        save = hvac_kwh * 0.08 * tariff
        recommendations.append(
            _rec(
                "High HVAC usage",
                "HVAC systems account for over 35% of estimated load. Consider VFD drives, "
                "setpoint optimization, and night setback schedules.",
                save,
                "High",
                "High",
            )
        )

    # Inefficient lighting
    light_kwh = by_cat.get("light", 0)
    if light_kwh > 0 and light_kwh / total_device_kwh > 0.12:
        save = light_kwh * 0.4 * tariff
        recommendations.append(
            _rec(
                "Inefficient lighting",
                "Lighting share is high. Upgrade to LED with occupancy sensors in corridors "
                "and meeting rooms.",
                save,
                "Medium",
                "Medium",
            )
        )

    # Standby losses
    standby_total = sum(
        (float(d.standby_watts or 0) * int(d.quantity or 1) * 24 * int(d.days_per_month or 30))
        / 1000
        for d in devices
    )
    if standby_total > 50:
        save = standby_total * 0.5 * tariff
        recommendations.append(
            _rec(
                "High standby losses",
                f"Standby loads estimate ~{standby_total:.0f} kWh/month. Use smart power strips "
                "and shutdown policies for TVs, chargers, and office equipment.",
                save,
                "Medium",
                "Medium",
            )
        )

    # Server / data center
    server_kwh = by_cat.get("server", 0) + by_cat.get("computer", 0) * 0.3
    if server_kwh > 200:
        save = server_kwh * 0.1 * tariff
        recommendations.append(
            _rec(
                "Server / data center load",
                "IT infrastructure shows significant consumption. Evaluate virtualization, "
                "hot/cold aisle containment, and PUE monitoring.",
                save,
                "High",
                "High",
            )
        )

    # Pumps and lifts — long operating hours
    for d in devices:
        cat = (d.category or "").lower()
        if cat in ("pump", "lift") and float(d.hours_per_day or 0) > 12:
            kwh = device_total_monthly_kwh(d)
            save = kwh * 0.07 * tariff
            recommendations.append(
                _rec(
                    f"High runtime: {d.name}",
                    f"{d.category} runs {d.hours_per_day}h/day. Review scheduling, soft-start, "
                    "and load sharing to cut peak demand.",
                    save,
                    "Medium",
                    "Medium",
                )
            )
            break

    # Abnormal device usage — very high hours
    for d in devices:
        if float(d.hours_per_day or 0) > 20 and (d.category or "").lower() not in ("server", "ups"):
            kwh = device_total_monthly_kwh(d)
            save = kwh * 0.05 * tariff
            recommendations.append(
                _rec(
                    f"Abnormal usage: {d.name}",
                    f"{d.name} is logged at {d.hours_per_day} hours/day. Verify timers and "
                    "automation — may indicate data entry error or waste.",
                    save,
                    "Low",
                    "Low",
                )
            )
            break

    # Power factor
    if float(building.power_factor or 1) < 0.9:
        save = monthly_bill * 0.03
        recommendations.append(
            _rec(
                "Power factor improvement",
                "Power factor below 0.9 can increase demand charges. Install capacitor banks "
                "or active PFC on large motor loads.",
                save,
                "High",
                "Medium",
            )
        )

    # Demand factor optimization
    if float(building.demand_factor or 1) > 0.9:
        save = monthly_bill * 0.04
        recommendations.append(
            _rec(
                "Demand factor optimization",
                "Demand factor is high — peak and average load are close. Stagger HVAC and "
                "kitchen equipment start times to reduce peak kVA.",
                save,
                "Medium",
                "Medium",
            )
        )

    # Benchmark comparison
    bench = compare_to_benchmark(
        total_kwh, building.building_type, building.building_area
    )
    if bench["status"] == "above_benchmark":
        save = (total_kwh - bench["expected"]) * 0.1 * tariff
        recommendations.append(
            _rec(
                "Above industry benchmark",
                f"Usage is ~{bench['variance_pct']}% above typical {building.building_type} "
                f"benchmarks. Prioritize an energy audit on top three categories.",
                max(save, 0),
                "High",
                "High",
            )
        )

    # Solar recommendation
    gen = solar_monthly_generation_kwh(building.solar_kw, building.peak_sun_hours)
    if float(building.solar_kw or 0) < 10 and total_kwh > 500:
        potential_kw = min(total_kwh / (float(building.peak_sun_hours or 5) * 30), 500)
        potential_gen = solar_monthly_generation_kwh(potential_kw, building.peak_sun_hours)
        grid = reduced_grid_kwh(total_kwh, potential_gen)
        new_bill = reduced_monthly_bill(grid, tariff)
        save = monthly_savings(monthly_bill, new_bill)
        recommendations.append(
            _rec(
                "Solar system recommendation",
                f"A ~{potential_kw:.0f} kW rooftop array could offset a meaningful share of "
                "grid imports. Validate with site survey and net-metering rules.",
                save,
                "High",
                "High",
            )
        )
    elif gen > 0 and solar_summary and solar_summary.get("savings_percentage", 0) < 15:
        recommendations.append(
            _rec(
                "Expand solar capacity",
                "Current solar size yields modest savings. Consider additional kW if roof "
                "area and budget allow.",
                monthly_bill * 0.05,
                "Medium",
                "Medium",
            )
        )

    if not recommendations:
        recommendations.append(
            _rec(
                "Maintain efficient operations",
                "No major rule triggers detected. Continue monitoring monthly kWh and "
                "re-calibrate after equipment changes.",
                0,
                "Low",
                "Low",
            )
        )

    # Sort: High priority first, then by savings
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(
        key=lambda r: (priority_order.get(r["priority"], 9), -r["estimated_savings"])
    )
    return recommendations


def persist_recommendations(building_id, rec_list, db, Recommendation):
    """Clear old recommendations and save new ones."""
    Recommendation.query.filter_by(building_id=building_id).delete()
    for item in rec_list:
        row = Recommendation(
            building_id=building_id,
            title=item["title"],
            message=item["message"],
            estimated_savings=item["estimated_savings"],
            priority=item["priority"],
            energy_impact=item["energy_impact"],
        )
        db.session.add(row)
    db.session.commit()
