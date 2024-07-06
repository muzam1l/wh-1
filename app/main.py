import os
import shutil
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from lib.google_vision import get_recommended_products_from_image
from lib.save_image import save_image_from_cdn
from . import crud, models, schemas
from .db import SessionLocal, engine
from ..lib.extractor import extract_images

models.Base.metadata.create_all(bind=engine)
from pathlib import Path

app = FastAPI()
OUTPUT_PATH = "downloaded"
OUTPUT_PATH_RESULT = "downloaded/result"
OUTPUT = Path(__file__).parent.parent / OUTPUT_PATH_RESULT


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
        elif media_type == "IMAGE":
            # Fetch directly
            for media_url in media_urls:
                save_image_from_cdn(media_url)

        if not OUTPUT.exists() or not OUTPUT.is_dir():
            print("No results found")
            return

        results = []

        for file_path in OUTPUT.iterdir():
            if file_path.is_file():
                with open(file_path, 'r') as file:
                    content = file.read()
                    results.extend(get_recommended_products_from_image(content))

        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        for result in sorted_results:
            print('Product ID: {}'.format(result.product.name))
            print('Score: {}'.format(result.score))

        return "Success"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
