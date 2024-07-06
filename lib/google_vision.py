from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# echo 'export GOOGLE_APPLICATION_CREDENTIALS="/Users/harshitanahta/Work/wishlink-google-vision-prodcut-api.json"' >> ~/.zshrc

client = vision_v1.ProductSearchClient()
image_annotator_client = vision_v1.ImageAnnotatorClient()


project_id = 'wishlink-product-search'
location = 'asia-east1'
product_set_id = 'FINAL'
product_set_path = client.product_set_path(project_id, location, product_set_id)

def get_recommended_products_from_image(content):
    # with open(image_path, 'rb') as image_file:
    #     content = image_file.read()
    image = types.Image(content=content)
    search_params = types.ProductSearchParams(
        product_set=product_set_path,
        product_categories=['apparel-v2'],
    )
    request = types.AnnotateImageRequest(
        image=image,
        features=[types.Feature(type=vision_v1.Feature.Type.PRODUCT_SEARCH)],
        image_context=types.ImageContext(product_search_params=search_params)
    )
    response = image_annotator_client.batch_annotate_images(requests=[request])
    return response.responses[0].product_search_results.results







