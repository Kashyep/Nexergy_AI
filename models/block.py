"""Block model — wing or zone within a building."""
from models import db


class Block(db.Model):
    __tablename__ = "blocks"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
