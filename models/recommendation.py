"""Recommendation model — persisted AI-style energy tips."""
from datetime import datetime

from models import db


class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    estimated_savings = db.Column(db.Float, default=0.0)
    priority = db.Column(db.String(20), default="Medium")
    energy_impact = db.Column(db.String(20), default="Medium")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
