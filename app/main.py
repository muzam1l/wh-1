from typing import Annotated, Literal
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine
from . import crud, models, schemas
from ..lib.extractor import extract_images

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
def read_root():
    return "pong"


@app.get("/get_recommended_products/{media_id}", response_model=schemas.StrIds)
def get_recommended_products(media_id: int, db: Session = Depends(get_db)):
    ids = crud.get_recommended_product_ids(db, media_id)

    return {"ids": ids}


@app.post("/create_recommended_products", response_model=None)
def create_recommended_products(
    media_id: int,
    media_urls: list[str],
    media_type: Literal["IMAGE", "VIDEO", "CAROUSEL_ALBUM"],
    db: Session = Depends(get_db),
):
    try:
        if media_type == "VIDEO":
            url = media_urls[0]
            extract_images(url)

            # = use images in /result
        else:
            pass
            # use media_urls directly

        return "Success"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
