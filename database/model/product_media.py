from database import db


class ProductMedia(db.Model):
    __tablename__ = "product_media"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )

    product = db.relationship(
        "Product", back_populates="medias", overlaps="product_medias"
    )

    def __repr__(self):
        return (
            f"<ProductMedia id={self.id} product_id={self.product_id} path={self.path}>"
        )
