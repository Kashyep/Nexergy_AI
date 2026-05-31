"""Floor model — floor level within a building or block."""
from models import db


class Floor(db.Model):
    __tablename__ = "floors"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.id"), nullable=True)
    floor_number = db.Column(db.Integer, nullable=False)
