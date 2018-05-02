import argparse
import json
from flask import Flask
from flask import render_template
from db import DB

app = Flask(__name__)


def parse_arguments():
    """
    Parse arguments from command line and return the results.
    :return: parsed args
    """
    parser = argparse.ArgumentParser(description="SOQ Management Web Backend.")
    parser.add_argument("--debug", action="store_true",
                        help="Use this option to enable debug mode.")
    parser.add_argument("--host", action='store', default="redis",
                        help="Specify Redis host address.")
    parser.add_argument("--port", action='store', default=6379, type=int,
                        help="Specify Redis host port.")
    return parser.parse_args()


@app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route("/")
def view_index():
    text_queue_count = db.get_text_queue_count()
    result_set_count = db.get_result_set_count()
    return render_template(
        "home.html",
        text_queue_count=text_queue_count,
        result_set_count=result_set_count
    )


@app.route("/result", defaults={"page": 1})
@app.route("/result/page/<int:page>")
def view_result(page):
    results = db.get_results(10 * (page - 1), 10)
    return json.dumps(results)


@app.route("/api")
def view_api():
    return render_template("api.html")


if __name__ == "__main__":
    args = parse_arguments()
    db = DB(args.host, args.port)
    app.run(host="0.0.0.0", debug=args.debug)
