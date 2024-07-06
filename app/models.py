from sqlalchemy import Column, Integer, String, Float

from .db import Base


class ProductRecommendations(Base):
    __tablename__: str = "productrecommendations"
    id = Column(Integer, primary_key=True)

    product_id = Column(String, index=True)
    media_id = Column(String, index=True)
    score = Column(Float(precision=6), index=True)
