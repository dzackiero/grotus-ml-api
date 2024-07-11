from flask import Blueprint, jsonify, request
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer
import torch
from deep_translator import GoogleTranslator

from database.model.product import Product


def translate_text(text, target_language="en"):
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)


model_directory = "model/search"
loaded_model = DistilBertForSequenceClassification.from_pretrained(model_directory)
loaded_tokenizer = DistilBertTokenizer.from_pretrained(model_directory)
bp = Blueprint("search", __name__)

labels = {0: "Potassium", 1: "Nitrogen", 2: "Phosphor"}


@bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("filter[search]", "")
    text = translate_text(query)

    inputs = loaded_tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = loaded_model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)

    result = labels[predictions.item()]
    products = getProducts(result)

    return (
        jsonify({"query": query, "text": text, "result": result, "products": products}),
        200,
    )


def getProducts(label):
    product_ids = [
        product.id
        for product in Product.query.filter(
            Product.nutrition_types.any(name=label)
        ).all()
    ]
    products = Product.query.filter(Product.id.in_(product_ids)).all()

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

    return data
