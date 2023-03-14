import requests
from pathlib import Path
import os

TOKEN = os.environ.get("COVIGILANCE_TOKEN")
ENDPOINT = os.environ.get("COVIGILANCE_API_ENDPOINT",
                          "https://api.covigilance.ai")


def upload_pdf(path: Path, product: str, id=None, token=TOKEN, endpoint=ENDPOINT):
    """
    Uploading a single pdf to covigilance.ai. It uses multipart form upload to upload the data.

    Parameters:
    path: Path - Path on the local file system to a pdf file
    product: str - Product the article should be analyzed for
    id: Optional(str) - Identifier for the article. If non provided will default to the filename
    """
    if id is None:
        id = ".".join(path.name.split(".")[:-1])
    body = {
        'file': (path.name, open(path, "rb")),
        'id': (None, id),
        'product': (None, product),
    }

    return requests.post(f"{endpoint}/upload-pdf", files=body, auth=BearerAuth(token)).json()


def upload_folder(path: Path, product: str, token=TOKEN, endpoint=ENDPOINT):
    """
    Uploads all pdf in a path to covigilance.ai. The current implementation is blocking for an easier code to get into.
    The API is not limited to sequential uploads and can accept multiple connections at once. This implementation assumes
    all files in the target will be analyzed for the same product.

    Parameters:
    path: Path - Path to a folder on the local file system containing the pdf
    product: str - Product the articles should be analyzed for
    """
    res = []
    for pdf in path.glob("*.pdf"):
        partial_result = upload_pdf(
            pdf, product=product, token=token, endpoint=endpoint)
        res.append(partial_result)
    return res


class BearerAuth(requests.auth.AuthBase):
    """
    This class helps with injecting the authorization token into the request
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
