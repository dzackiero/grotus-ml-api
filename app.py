from flask import Flask
from config import CONFIG

# from blueprints.detection import bp as detection_bp
from blueprints.index import bp as index_bp
from blueprints.recommendation import bp as recommend_bp


from database import db, Product, NutritionType, nutrition_type_product


def create_app():
    app = Flask(__name__)
    app.config.update(CONFIG)

    # Initializing
    db.init_app(app)

    # Bluprints
    app.register_blueprint(index_bp)
    app.register_blueprint(recommend_bp)
    # app.register_blueprint(detection_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
