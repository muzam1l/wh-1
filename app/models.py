from sqlalchemy import Column, String, Float

from .db import Base


class ProductRecommendations(Base):
    __tablename__: str = "productrecommendations"

    id = Column(String, primary_key=True)
    media_id = Column(String, index=True)
    score = Column(Float(precision=6), index=True)
