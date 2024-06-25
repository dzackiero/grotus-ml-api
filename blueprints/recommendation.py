from database.model.product import Product
from flask import Blueprint, jsonify, request
import pandas as pd

from utils.sys_recomendation import SysRecommendation


bp = Blueprint("recommendation", __name__)


@bp.route("/recommend")
def recommend():
    recSys = SysRecommendation(generate_products_dataframe(), "metadata")
    recSys.fit()
    df_rec = recSys.predict(1, 200)
    return jsonify(df_rec.to_dict(orient="records"))


@bp.route("/frame")
def frame():
    df = generate_products_dataframe()
    return jsonify(df.to_dict(orient="records"))


def generate_products_dataframe():
    # Query all products
    products = Product.query.all()

    # Prepare the data
    data = []
    for product in products:
        nutrition_types = [
            {"id": nt.id, "name": nt.name} for nt in product.nutrition_types
        ]
        data.append(
            {
                "id": product.id,
                "name": product.name,
                "nutrition_types": nutrition_types,
                "type": product.type.name,
                "description": product.description,
                "metadata": product.meta_data,
            }
        )

    # Create a DataFrame
    df = pd.DataFrame(data)

    return df
