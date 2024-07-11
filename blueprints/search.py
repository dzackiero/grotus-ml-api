from flask import Blueprint, jsonify, request
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer
import torch
from deep_translator import GoogleTranslator


def translate_text(text, target_language="en"):
    translator = GoogleTranslator(source="auto", target=target_language)
    return translator.translate(text)


model_directory = "model/search"
loaded_model = DistilBertForSequenceClassification.from_pretrained(model_directory)
loaded_tokenizer = DistilBertTokenizer.from_pretrained(model_directory)
bp = Blueprint("search", __name__)

labels = {0: "Potassium", 1: "Nitrogen", 2: "Phosphor"}


@bp.route("/search", methods=["GET"])
def predict():
    query = request.args.get("filter[search]", "")
    text = translate_text(query)

    inputs = loaded_tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = loaded_model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)

    return (
        jsonify({"query": query, "text": text, "result": labels[predictions.item()]}),
        200,
    )
