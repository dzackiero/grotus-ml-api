from database import db
from sqlalchemy.dialects.mysql import LONGTEXT

nutrition_type_product = db.Table(
    "nutrition_type_product",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column(
        "nutrition_type_id",
        db.Integer,
        db.ForeignKey("nutrition_types.id"),
        primary_key=True,
    ),
)
