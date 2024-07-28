from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .model.product import Product
from .model.product_media import ProductMedia
from .model.nutrition_type import NutritionType
from .model.nutrition_type_product import nutrition_type_product
