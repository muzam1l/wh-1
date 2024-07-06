from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    productrecommendations = relationship("ProductRecommendations", back_populates="media")


class ProductRecommendations(Base):
    __tablename__: str = "productrecommendations"

    id = Column(String, primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id"))
    media = relationship("Media", back_populates="productrecommendations")
