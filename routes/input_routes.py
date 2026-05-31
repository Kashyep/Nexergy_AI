"""Energy input form — save building and multiple devices."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import db
from models.building import Building
from models.device import Device

input_bp = Blueprint("input", __name__, url_prefix="/input")

DEVICE_CATEGORIES = [
    "HVAC",
    "Air conditioner",
    "Chiller",
    "AHU",
    "Fan",
    "Refrigerator",
    "TV",
    "Light",
    "Computer",
    "Server",
    "Washing machine",
    "Charger",
    "Lift",
    "Pump",
    "Medical equipment",
    "Kitchen equipment",
    "UPS",
    "Other",
]

BUILDING_TYPES = [
    "hospital",
    "software company",
    "mall",
    "college",
    "hotel",
    "office",
    "residential apartment",
    "campus",
]


def _float(name, default=0.0):
    try:
        return float(request.form.get(name, default) or default)
    except (TypeError, ValueError):
        return default


def _int(name, default=0):
    try:
        return int(request.form.get(name, default) or default)
    except (TypeError, ValueError):
        return default


def _bool(name):
    return request.form.get(name) in ("on", "true", "1", "yes")


def load_sample_hospital():
    """Create a demo hospital dataset (replaces existing data)."""
    from models.recommendation import Recommendation

    Recommendation.query.delete()
    Device.query.delete()
    Building.query.delete()
    db.session.commit()

    building = Building(
        name="City Care Hospital",
        building_type="hospital",
        building_area=85000,
        num_occupants=420,
        num_blocks=4,
        num_floors=8,
        tariff_rate=9.5,
        voltage=415,
        current=1200,
        power_factor=0.88,
        demand_factor=0.82,
        diversity_factor=0.88,
        solar_kw=150,
        peak_sun_hours=5.2,
    )
    db.session.add(building)
    db.session.flush()

    sample_devices = [
        ("Central Chiller", "Chiller", "Block A", 1, "HVAC Plant", 450000, 2, 18, 30, 0.9, 500, 0.85, True),
        ("ICU AHU", "AHU", "Block B", 3, "ICU", 22000, 4, 24, 30, 0.88, 200, 0.9, True),
        ("LED Ward Lighting", "Light", "Block A", 2, "Wards", 40, 1200, 14, 30, 1.0, 2, 0.95, False),
        ("MRI Suite", "Medical equipment", "Block C", 1, "Radiology", 35000, 1, 10, 26, 0.95, 800, 0.9, True),
        ("Data Center Rack", "Server", "Block D", 2, "IT", 8000, 40, 24, 30, 0.99, 150, 0.92, True),
        ("Main Lift Bank", "Lift", "Block A", 1, "Vertical Transport", 18000, 6, 16, 30, 0.85, 100, 0.8, False),
        ("Booster Pump", "Pump", "Block A", 0, "Utilities", 7500, 3, 12, 30, 0.8, 50, 0.75, True),
        ("Kitchen Freezer", "Refrigerator", "Block B", 1, "Cafeteria", 1200, 8, 20, 30, 0.9, 30, 0.85, False),
    ]

    for row in sample_devices:
        d = Device(
            building_id=building.id,
            name=row[0],
            category=row[1],
            block_name=row[2],
            floor_number=row[3],
            zone=row[4],
            wattage=row[5],
            quantity=row[6],
            hours_per_day=row[7],
            days_per_month=row[8],
            power_factor=row[9],
            standby_watts=row[10],
            efficiency_rating=row[11],
            is_critical=row[12],
        )
        db.session.add(d)

    db.session.commit()
    return building.id


def load_sample_software_company():
    """Create a demo software campus dataset."""
    from models.recommendation import Recommendation

    Recommendation.query.delete()
    Device.query.delete()
    Building.query.delete()
    db.session.commit()

    building = Building(
        name="Nexergy Tech Campus",
        building_type="software company",
        building_area=45000,
        num_occupants=800,
        num_blocks=2,
        num_floors=6,
        tariff_rate=8.75,
        voltage=415,
        current=650,
        power_factor=0.92,
        demand_factor=0.78,
        diversity_factor=0.9,
        solar_kw=80,
        peak_sun_hours=5.5,
    )
    db.session.add(building)
    db.session.flush()

    sample_devices = [
        ("VRF AC Plant", "Air conditioner", "Tower 1", 3, "Open Office", 85000, 3, 12, 30, 0.9, 300, 0.88, False),
        ("Workstation PCs", "Computer", "Tower 1", 2, "Engineering", 150, 600, 10, 22, 1.0, 5, 0.9, False),
        ("Server Room", "Server", "Tower 2", 1, "DC", 12000, 25, 24, 30, 0.99, 200, 0.93, True),
        ("LED Office Lights", "Light", "Tower 1", 4, "All Floors", 35, 2000, 11, 22, 1.0, 1, 0.96, False),
        ("EV Charger Hub", "Charger", "Parking", 0, "Parking", 7000, 10, 6, 26, 1.0, 20, 0.9, False),
        ("Cafeteria HVAC", "HVAC", "Tower 2", 1, "Cafeteria", 25000, 2, 14, 30, 0.88, 150, 0.87, False),
    ]

    for row in sample_devices:
        d = Device(
            building_id=building.id,
            name=row[0],
            category=row[1],
            block_name=row[2],
            floor_number=row[3],
            zone=row[4],
            wattage=row[5],
            quantity=row[6],
            hours_per_day=row[7],
            days_per_month=row[8],
            power_factor=row[9],
            standby_watts=row[10],
            efficiency_rating=row[11],
            is_critical=row[12],
        )
        db.session.add(d)

    db.session.commit()
    return building.id


@input_bp.route("/", methods=["GET", "POST"])
def energy_input():
    """Show form or process building + device submission."""
    if request.method == "GET":
        sample = request.args.get("sample")
        if sample == "hospital":
            load_sample_hospital()
            flash("Sample hospital dataset loaded. View the dashboard!", "success")
            return redirect(url_for("dashboard.dashboard"))
        if sample == "software":
            load_sample_software_company()
            flash("Sample software company dataset loaded. View the dashboard!", "success")
            return redirect(url_for("dashboard.dashboard"))

        return render_template(
            "input.html",
            categories=DEVICE_CATEGORIES,
            building_types=BUILDING_TYPES,
        )

    # POST — validate required building fields
    building_type = request.form.get("building_type", "").strip()
    building_area = _float("building_area")
    tariff_rate = _float("tariff_rate")

    if not building_type:
        flash("Please select a building type.", "error")
        return redirect(url_for("input.energy_input"))
    if building_area <= 0:
        flash("Building area must be greater than zero.", "error")
        return redirect(url_for("input.energy_input"))
    if tariff_rate <= 0:
        flash("Tariff rate must be greater than zero.", "error")
        return redirect(url_for("input.energy_input"))

    # Replace previous session data (single-building demo app)
    from models.recommendation import Recommendation

    Recommendation.query.delete()
    Device.query.delete()
    Building.query.delete()
    db.session.commit()

    building = Building(
        name=request.form.get("building_name", "My Building").strip() or "My Building",
        building_type=building_type,
        building_area=building_area,
        num_occupants=_int("num_occupants", 0),
        num_blocks=_int("num_blocks", 1),
        num_floors=_int("num_floors", 1),
        tariff_rate=tariff_rate,
        voltage=_float("voltage", 415),
        current=_float("current", 0),
        power_factor=_float("power_factor", 0.9),
        demand_factor=_float("demand_factor", 0.85),
        diversity_factor=_float("diversity_factor", 0.9),
        solar_kw=_float("solar_kw", 0),
        peak_sun_hours=_float("peak_sun_hours", 5),
    )
    db.session.add(building)
    db.session.flush()

    names = request.form.getlist("device_name[]")
    if not names or not any(n.strip() for n in names):
        flash("Add at least one device before submitting.", "error")
        db.session.rollback()
        return redirect(url_for("input.energy_input"))

    categories = request.form.getlist("device_category[]")
    blocks = request.form.getlist("device_block[]")
    floors = request.form.getlist("device_floor[]")
    zones = request.form.getlist("device_zone[]")
    wattages = request.form.getlist("device_wattage[]")
    quantities = request.form.getlist("device_quantity[]")
    hours = request.form.getlist("device_hours[]")
    days = request.form.getlist("device_days[]")
    pfs = request.form.getlist("device_pf[]")
    standbys = request.form.getlist("device_standby[]")
    efficiencies = request.form.getlist("device_efficiency[]")
    for i, name in enumerate(names):
        name = name.strip()
        if not name:
            continue
        try:
            wattage = float(wattages[i] if i < len(wattages) else 0)
        except (TypeError, ValueError):
            wattage = 0
        if wattage <= 0:
            continue

        device = Device(
            building_id=building.id,
            name=name,
            category=categories[i] if i < len(categories) else "Other",
            block_name=blocks[i] if i < len(blocks) else "Main",
            floor_number=int(floors[i]) if i < len(floors) and str(floors[i]).isdigit() else 1,
            zone=zones[i] if i < len(zones) else "General",
            wattage=wattage,
            quantity=int(quantities[i]) if i < len(quantities) and str(quantities[i]).isdigit() else 1,
            hours_per_day=float(hours[i]) if i < len(hours) else 8,
            days_per_month=int(days[i]) if i < len(days) and str(days[i]).isdigit() else 30,
            power_factor=float(pfs[i]) if i < len(pfs) else 1.0,
            standby_watts=float(standbys[i]) if i < len(standbys) else 0,
            efficiency_rating=float(efficiencies[i]) if i < len(efficiencies) else 1.0,
            is_critical=_bool(f"device_critical_{i}"),
        )
        db.session.add(device)

    db.session.commit()
    flash("Energy data saved successfully!", "success")
    return redirect(url_for("dashboard.dashboard"))
