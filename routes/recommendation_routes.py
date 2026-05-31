"""AI recommendations page."""
from flask import Blueprint, flash, render_template

from models.building import Building
from models.device import Device
from models.recommendation import Recommendation
from models import db
from routes.input_routes import load_sample_hospital
from services.ai_recommendation import generate_recommendations, persist_recommendations
from services.energy_calculator import building_summary
from services.solar_calculator import solar_comparison

recommendation_bp = Blueprint("recommendations", __name__, url_prefix="/recommendations")


@recommendation_bp.route("/")
def recommendations():
    building = Building.query.order_by(Building.id.desc()).first()

    if not building:
        load_sample_hospital()
        flash("Sample data loaded to generate recommendations.", "info")
        building = Building.query.order_by(Building.id.desc()).first()

    devices = Device.query.filter_by(building_id=building.id).all()
    summary = building_summary(building, devices)
    solar = solar_comparison(
        building,
        summary["adjusted_monthly_kwh"],
        summary["monthly_bill"],
    )

    rec_list = generate_recommendations(building, devices, summary, solar)
    persist_recommendations(building.id, rec_list, db, Recommendation)

    stored = Recommendation.query.filter_by(building_id=building.id).all()
    total_savings = sum(r.estimated_savings for r in stored)

    return render_template(
        "recommendations.html",
        building=building,
        recommendations=stored,
        summary=summary,
        total_savings=round(total_savings, 2),
    )
