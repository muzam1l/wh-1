from sqlalchemy.orm import Session
from . import models


def get_recommended_product_ids(db: Session, media_id: int):
    return db.query(models.ProductRecommendations.id).filter(
        models.ProductRecommendations.media_id == media_id
    )
