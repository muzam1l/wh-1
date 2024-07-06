from sqlalchemy.orm import Session
from . import models


def get_recommended_product_ids(db: Session, media_id: str):
    return (
        db.query(models.ProductRecommendations.product_id)
        .filter(models.ProductRecommendations.media_id == media_id)
        .order_by(models.ProductRecommendations.score.desc())
        .distinct(models.ProductRecommendations.score)
    )
