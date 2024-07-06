from os import environ
from pathlib import Path
from typing import Any
import urllib3

UPLOADTHING_SECRET = environ.get("UPLOADTHING_SECRET") or ""
url = "https://api.uploadthing.com/v6/uploadFiles"


def get_presigned_url(file: dict) -> dict[str, Any]:
    res = urllib3.request(
        "POST",
        url,
        headers={
            "x-uploadthing-api-key": UPLOADTHING_SECRET,
        },
        json={
            "contentDisposition": "inline",
            "acl": "public-read",
            "files": [file],
        },
    )

    return res.json()["data"][0]


def upload_file(prefix: str, file_path: str):
    with open(file_path, "rb") as file:
        file_content = file.read()
        name = Path(prefix, file_path).as_posix()

        file = {
            "name": name,
            "size": len(file_content),
            "type": "image/jpeg",
        }

        presined = get_presigned_url(file)
        
        url = presined["url"]
        fields: dict = presined["fields"]
        fields["file"] = file_content

        print("got presigned url", url)
        res = urllib3.request(
            "POST",
            url,
            fields=fields,
        )

        if res.status < 400:
            print(f"File upload successful for {file_path}")
        else:
            print(
                f"Error: Unable to upload file. Status Code: {res.status}: {res.data.decode('utf-8')}"
            )

