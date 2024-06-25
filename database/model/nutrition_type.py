from database import db


class NutritionType(db.Model):
    __tablename__ = "nutrition_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<NutritionType(id={self.id}, name='{self.name}', created_at={self.created_at}, updated_at={self.updated_at})>"
