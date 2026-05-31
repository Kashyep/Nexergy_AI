"""
Register all Flask blueprints for Nexergy AI.
"""


def register_blueprints(app):
    from routes.home_routes import home_bp
    from routes.input_routes import input_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.recommendation_routes import recommendation_bp
    from routes.solar_routes import solar_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(input_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(solar_bp)
