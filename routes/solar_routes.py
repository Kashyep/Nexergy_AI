"""Solar comparison page."""
from flask import Blueprint, flash, render_template
import json

from models.building import Building
from models.device import Device
from routes.input_routes import load_sample_hospital
from services.energy_calculator import building_summary
from services.solar_calculator import solar_comparison

solar_bp = Blueprint("solar", __name__, url_prefix="/solar")


@solar_bp.route("/")
def solar_page():
    building = Building.query.order_by(Building.id.desc()).first()

    if not building:
        load_sample_hospital()
        flash("Sample data loaded for solar comparison.", "info")
        building = Building.query.order_by(Building.id.desc()).first()

    devices = Device.query.filter_by(building_id=building.id).all()
    summary = building_summary(building, devices)
    solar = solar_comparison(
        building,
        summary["adjusted_monthly_kwh"],
        summary["monthly_bill"],
    )

    chart_data = {
        "labels": ["Grid Bill (No Solar)", "Bill After Solar"],
        "bills": [solar["current_monthly_bill"], solar["reduced_monthly_bill"]],
        "kwh": [
            summary["adjusted_monthly_kwh"],
            solar["grid_kwh_after_solar"],
        ],
        "generation": solar["solar_monthly_generation_kwh"],
    }

    return render_template(
        "solar.html",
        building=building,
        summary=summary,
        solar=solar,
        chart_data_json=json.dumps(chart_data),
    )
