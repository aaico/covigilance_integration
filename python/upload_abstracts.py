import requests
import pandas as pd
import json
from pathlib import Path
import os

TOKEN = os.environ.get("COVIGILANCE_TOKEN")
ENDPOINT = os.environ.get("COVIGILANCE_API_ENDPOINT",
                          "https://api.covigilance.ai")


class BearerAuth(requests.auth.AuthBase):
    """
    This class helps with injecting the authorization token into the request
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def upload_abstracts(abstracts, token=TOKEN, endpoint=ENDPOINT):
    """
    Upload a dictionary (json) to the abstract endpoint of Covigilance.ai.

    The abstracts are a list of items of the form
    {'id': string,
     'title': string,
     'abstract': string,
     'product': string}
    """
    return requests.post(f"{endpoint}/upload-abstracts", json={"abstracts": abstracts}, auth=BearerAuth(token)).json()


def read_csv(path: Path):
    """
    Helping function to read a csv and convert it into a dictionary (json) structure
    """
    df = pd.read_csv(path, sep=";")
    records = df.to_dict(orient="records")
    return records


def read_excel(path: Path):
    """
    Helping function to read an excel sheet and convert it into a dictionary (json) structure
    """
    df = pd.read_excel(path)
    records = df.to_dict(orient="records")
    return records


def prepare_record(record, pos=0, prefix="", fields=["product", "title", "abstract"]):
    """
    Helping function to prepare the json.

    The function will strip unnecessary keys from the structure and injects an identifier
    if non yet exists.
    """
    if "id" not in record:
        record["id"] = prefix + "-" + str(pos)
    fields.append("id")
    return {k.lower(): v for k, v in record.items() if k.lower() in fields}


def load_abstracts(path: Path, start=0, length=None):
    """
    A general method to load abstracts from a file.
    Currently supports Excel (.xls, .xlsx), CSV (.csv) and JSON.

    Returns a processed dictionary, that is read to be passed to the Covigilance API.
    """
    if path.name.endswith(".xls") or path.name.endswith(".xlsx"):
        abstracts = read_excel(path)
    elif path.name.endswith(".csv"):
        abstracts = read_csv(path)
    else:
        abstracts = json.loads(path.read_text())
    name = ".".join(path.name.split(".")[:-1])
    abstracts = [prepare_record(a, pos=i, prefix=name)
                 for i, a in enumerate(abstracts)]
    if length:
        return abstracts[start:start+length]
    else:
        return abstracts[start:]
