"""
SQLAlchemy database instance and model imports.
Import models here so Flask-SQLAlchemy registers them before create_all().
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is created (registers tables with metadata)
from models.building import Building  # noqa: E402, F401
from models.block import Block  # noqa: E402, F401
from models.floor import Floor  # noqa: E402, F401
from models.device import Device  # noqa: E402, F401
from models.recommendation import Recommendation  # noqa: E402, F401
