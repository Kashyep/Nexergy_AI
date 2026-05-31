"""Device model — individual load item with usage profile."""
from models import db


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    block_name = db.Column(db.String(120), default="Main")
    floor_number = db.Column(db.Integer, default=1)
    zone = db.Column(db.String(120), default="General")
    wattage = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    hours_per_day = db.Column(db.Float, default=8.0)
    days_per_month = db.Column(db.Integer, default=30)
    power_factor = db.Column(db.Float, default=1.0)
    standby_watts = db.Column(db.Float, default=0.0)
    efficiency_rating = db.Column(db.Float, default=1.0)
    is_critical = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "block_name": self.block_name,
            "floor_number": self.floor_number,
            "zone": self.zone,
            "wattage": self.wattage,
            "quantity": self.quantity,
            "hours_per_day": self.hours_per_day,
            "days_per_month": self.days_per_month,
            "power_factor": self.power_factor,
            "standby_watts": self.standby_watts,
            "efficiency_rating": self.efficiency_rating,
            "is_critical": self.is_critical,
        }
