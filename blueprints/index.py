import csv
from io import StringIO
from flask import Blueprint, jsonify, make_response
from database.model.product import Product

bp = Blueprint("index", __name__)


@bp.route("/")
def index():
    return "<h3>Grotus Machine Learning Flask App</h3>"


@bp.route("/model")
def check_model():
    # Query the database
    products = Product.query.all()
    products_data = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "description": product.description,
            "type": product.type.name,
            "metadata": product.meta_data,
            "nutrition_types": [
                {"id": nt.id, "name": nt.name} for nt in product.nutrition_types
            ],
        }
        products_data.append(product_data)

    return jsonify(products_data)


@bp.route("/export")
def export():
    # Query all products
    products = Product.query.all()

    # Create a StringIO object to write CSV data to
    output = StringIO()
    writer = csv.writer(output)

    # Write the CSV header
    writer.writerow(
        [
            "Product_ID",
            "Product_Name",
            "Nutrition_Type",
            "Powder_or_Liquid",
            "Description",
            "Metadata",
        ]
    )

    # Write the product data
    for product in products:
        nutrition_types = ", ".join([nt.name for nt in product.nutrition_types])
        writer.writerow(
            [
                product.id,
                product.name,
                nutrition_types,
                product.type.name,
                product.description,
                product.meta_data,
            ]
        )

    # Prepare the response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    response.headers["Content-type"] = "text/csv"
    return response
