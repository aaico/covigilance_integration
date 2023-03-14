from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import logging
from typing import Union, List
import argparse
import uvicorn
import os
import requests

LOGGER = logging.getLogger(__name__)
TOKEN = os.environ.get("COVIGILANCE_TOKEN")
ENDPOINT = os.environ.get("COVIGILANCE_API_ENDPOINT",
                          "https://api.covigilance.ai")


def getWebhook(token=TOKEN, endpoint=ENDPOINT):
    """
    Get the currently registered webhook
    """
    return requests.get(f"{endpoint}/webhook", auth=BearerAuth(token)).json()


def setWebhook(url: str, token=TOKEN, endpoint=ENDPOINT):
    """
    Set the webhook to the provided url.
    """
    return requests.post(f"{endpoint}/webhook", data={"url": url}, auth=BearerAuth(token)).json()


class CovigilanceUpdate(BaseModel):
    """
    A response to an upload can have 2 message types:
    * Sucess: id, is_icsr, probability is set
    * Error: id, error is set

    Depending on the case you can update your internal models
    """
    id: str
    error: Union[str, None] = None
    is_icsr: Union[bool, None] = None
    probability: Union[float, None] = None


app = FastAPI()


@app.post("/")
async def root(updates: List[CovigilanceUpdate]):
    """
    Receive updates from the API and print them to the console.
    """
    for u in updates:
        if u.error is None:
            LOGGER.info(
                f"Received Update:\n  id={u.id}\n  ICSR={u.is_icsr}\n  probability={u.probability}")
        else:
            LOGGER.warning(
                f"Received an Error:\n  id={u.id}\n  Error={u.error}"
            )


class BearerAuth(requests.auth.AuthBase):
    """
    This class helps with injecting the authorization token into the request
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def start_webhook():
    parser = argparse.ArgumentParser(
        prog="covigilance-api webhook", description="Simple Server for testing the Webhook of Covigilance.ai"
    )

    parser.add_argument(
        "-t", "--token", help="Machine Authentication Token for the Covigilance API, defaults to the COVIGILANCE_TOKEN from the environment", required=False)
    parser.add_argument("-e", "--endpoint",
                        default="https://api-staging.covigilance.ai",
                        help="Endpoint of the Covigilance Backend")
    parser.add_argument("--url", required=True,
                        help="Public URL this services under which this service can be reached.")
    parser.add_argument("-p", "--port", type=int, default=5001,
                        help="Local Port to listen for responses from the backend.")
    parser.add_argument("webhook")

    parse = parser.parse_args()

    token = parse.token if parse.token else TOKEN

    try:
        previous_webhook = getWebhook(token=token, endpoint=parse.endpoint)
        setWebhook(parse.url, token=token, endpoint=parse.endpoint)
        uvicorn.run("webhook:app", host="0.0.0.0", port=parse.port)
    finally:
        url = previous_webhook.get("url", "")
        setWebhook(url, token=token, endpoint=parse.endpoint)
        print("Shutdown")
