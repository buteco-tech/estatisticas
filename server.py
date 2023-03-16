import os
import argparse

from ga4 import GoogleAnalyticsMetrics

from flask import Flask, render_template
from flask_cors import CORS


app = Flask(__name__)
app.config.from_prefixed_env()

CORS(app)


@app.route("/")
def index():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])

    data = {
        "pageviews": m.get_pageviews(),
        "acquisition": m.get_acquisition(),
        "top-pages": m.get_top_pages(),
        "top-oses": m.get_top_oses(),
        "top-contries": m.get_top_contries(),
        "top-browsers": m.get_top_browsers(),
    }

    return render_template("index.html", data=data)


@app.route("/stats/pageviews")
def pageviews():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_pageviews()


@app.route("/stats/acquisition")
def acquisition():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_acquisition()


@app.route("/stats/top-pages")
def top_pages():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_top_pages()


@app.route("/stats/top-oses")
def top_oses():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_top_oses()


@app.route("/stats/top-contries")
def top_contries():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_top_contries()


@app.route("/stats/top-browsers")
def top_browsers():
    m = GoogleAnalyticsMetrics(app.config["GA4_ID"], app.config["GA4_CREDENTIALS_PATH"])
    return m.get_top_browsers()


@app.route("/status")
def status():
    return {"status": "OK"}


def run_server():
    parser = argparse.ArgumentParser(prog="Stats")

    parser.add_argument("id", help="Google Analytics ID (v4)")
    parser.add_argument("credentials", help="Google Cloud credentials")
    parser.add_argument("-D", "--debug", action="store_true", help="run server in debug mode")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="server address")
    parser.add_argument("-P", "--port", type=int, default=5000, help="server port")

    args = parser.parse_args()

    app.config.update(
        {
            "GA4_ID": args.id,
            "GA4_CREDENTIALS_PATH": args.credentials,
        }
    )

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    run_server()
