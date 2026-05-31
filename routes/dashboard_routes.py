"""Dashboard — KPIs and chart data."""
import json

from flask import Blueprint, flash, render_template

from models.building import Building
from models.device import Device
from routes.input_routes import load_sample_hospital
from services.benchmark_data import compare_to_benchmark
from services.energy_calculator import building_summary, device_total_monthly_kwh
from services.solar_calculator import solar_comparison

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def _get_building_data():
    """Return latest building, devices, or None if empty."""
    building = Building.query.order_by(Building.id.desc()).first()
    if not building:
        return None, []
    devices = Device.query.filter_by(building_id=building.id).all()
    return building, devices


@dashboard_bp.route("/")
def dashboard():
    building, devices = _get_building_data()

    if not building:
        load_sample_hospital()
        flash("No data found — loaded sample hospital dataset for you.", "info")
        building, devices = _get_building_data()

    summary = building_summary(building, devices)
    solar = solar_comparison(
        building,
        summary["adjusted_monthly_kwh"],
        summary["monthly_bill"],
    )

    bench = compare_to_benchmark(
        summary["adjusted_monthly_kwh"],
        building.building_type,
        building.building_area,
    )

    device_rows = []
    for d in devices:
        kwh = device_total_monthly_kwh(d)
        device_rows.append(
            {
                "name": d.name,
                "category": d.category,
                "block": d.block_name,
                "zone": d.zone,
                "monthly_kwh": round(kwh, 2),
                "critical": d.is_critical,
            }
        )
    device_rows.sort(key=lambda x: x["monthly_kwh"], reverse=True)

    chart_data = {
        "by_device": summary["by_device"][:12],
        "by_category": summary["by_category"],
        "by_block": summary["by_block"],
        "solar_bills": {
            "labels": ["Current Bill", "After Solar"],
            "values": [solar["current_monthly_bill"], solar["reduced_monthly_bill"]],
        },
    }

    return render_template(
        "dashboard.html",
        building=building,
        summary=summary,
        solar=solar,
        benchmark=bench,
        device_rows=device_rows,
        chart_data_json=json.dumps(chart_data),
    )
