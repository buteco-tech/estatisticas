import os
import traceback

from sanic import Sanic
from sanic.response import json
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type",
}
AUTH_KEY_FILEPATH = os.getenv("AUTH_KEY_FILEPATH")
DEBUG = os.getenv("DEBUG") in ["1", "true", "yes"]

app = Sanic(__name__)

app.static("/", "./public/index.html", content_type="text/html; charset=utf-8")

def get_access_token():
  return ServiceAccountCredentials.from_json_keyfile_name(AUTH_KEY_FILEPATH, SCOPE).get_access_token().access_token

@app.route("/token")
async def token(request):
    try:
        token = get_access_token()
        return json({"token": token, "error": False}, headers=CORS_HEADERS)
    except Exception as e:
        traceback.print_exc()
        return json({"error": True}, status=500, headers=CORS_HEADERS)


@app.route("/status")
async def status(request):
    return json({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
