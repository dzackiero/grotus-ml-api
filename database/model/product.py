from database import db
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.mysql import LONGTEXT
from database.model.nutrition_type_product import nutrition_type_product
import enum


class ProductType(enum.Enum):
    powder = "powder"
    liquid = "liquid"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    type = db.Column(SAEnum(ProductType), nullable=False)
    meta_data = db.Column("metadata", LONGTEXT, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    nutrition_types = db.relationship(
        "NutritionType",
        secondary=nutrition_type_product,
        lazy="subquery",
        backref=db.backref("products", lazy=True),
    )

    def __repr__(self):
        return (
            f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock}, "
            f"description='{self.description}', type='{self.type}', metadata='{self.metadata}', "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
