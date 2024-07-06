import os
import requests
from urllib.parse import urlparse
from pathlib import Path

OUTPUT_PATH = "downloaded"
OUTPUT_PATH_RESULT = "downloaded/result"
OUTPUT = Path(__file__).parent.parent / OUTPUT_PATH_RESULT


def save_image_from_cdn(cdn_url: str):
    # Parse the URL to extract the filename
    parsed_url = urlparse(cdn_url)
    filename = os.path.basename(parsed_url.path)

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT, exist_ok=True)

    # Construct the file path
    file_path = os.path.join(OUTPUT, filename)

    try:
        # Send a GET request to download the image
        response = requests.get(cdn_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad response status

        # Write the image content to the file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Image saved successfully to: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {cdn_url}: {e}")
        return None
