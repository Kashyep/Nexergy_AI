"""Building model — stores large-facility metadata and electrical parameters."""
from datetime import datetime

from models import db


class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default="My Building")
    building_type = db.Column(db.String(80), nullable=False)
    building_area = db.Column(db.Float, nullable=False)
    num_occupants = db.Column(db.Integer, default=0)
    num_blocks = db.Column(db.Integer, default=1)
    num_floors = db.Column(db.Integer, default=1)
    tariff_rate = db.Column(db.Float, nullable=False)
    voltage = db.Column(db.Float, default=415.0)
    current = db.Column(db.Float, default=0.0)
    power_factor = db.Column(db.Float, default=0.9)
    demand_factor = db.Column(db.Float, default=0.85)
    diversity_factor = db.Column(db.Float, default=0.9)
    solar_kw = db.Column(db.Float, default=0.0)
    peak_sun_hours = db.Column(db.Float, default=5.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    blocks = db.relationship("Block", backref="building", lazy=True, cascade="all, delete-orphan")
    floors = db.relationship("Floor", backref="building", lazy=True, cascade="all, delete-orphan")
    devices = db.relationship("Device", backref="building", lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship(
        "Recommendation", backref="building", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "building_type": self.building_type,
            "building_area": self.building_area,
            "num_occupants": self.num_occupants,
            "num_blocks": self.num_blocks,
            "num_floors": self.num_floors,
            "tariff_rate": self.tariff_rate,
            "voltage": self.voltage,
            "current": self.current,
            "power_factor": self.power_factor,
            "demand_factor": self.demand_factor,
            "diversity_factor": self.diversity_factor,
            "solar_kw": self.solar_kw,
            "peak_sun_hours": self.peak_sun_hours,
        }
