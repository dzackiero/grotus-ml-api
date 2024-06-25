import csv
from io import StringIO
from flask import Blueprint, jsonify, make_response
from database.model.product import Product

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    return "<h3>Grotus Machine Learning Flask App</h3>"
