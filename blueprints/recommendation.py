from database.model.product import Product
from flask import Blueprint, jsonify, request
import pandas as pd

from utils.sys_recomendation import SysRecommendation


bp = Blueprint("recommendation", __name__)


@bp.route("/recommend/<int:productId>")
def recommend(productId):
    recSys = SysRecommendation(generate_products_dataframe(), "metadata")
    recSys.fit()

    limit = request.args.get("limit", default=10, type=int)
    df_rec = recSys.predict(productId, limit)
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
                "price": product.price,
                "stock": product.stock,
                "description": product.description,
                "type": product.type.name,
                "metadata": product.meta_data,
                "nutrition_types": nutrition_types,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
            }
        )

    # Create a DataFrame
    df = pd.DataFrame(data)

    return df
