import argparse
import os
import re
from flask import Flask
from flask import flash
from flask import request
from flask import render_template
from flask import abort
from db import DB
from helper import paginate
from helper import text_to_html

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


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


@app.route("/feed", methods=["GET", "POST"])
def feed():
    if request.method == "POST":
        # Push the text to queue.
        try:
            text = request.form["text"]
            uid = db.feed_text(text)
        except Exception as e:
            err = "An error occurred while pushing to queue: {}".format(e)
            print(err)
            flash(err, "danger")
        else:
            flash("Success! New Text UUID: {}".format(uid), "success")
    return render_template("feed.html")


@app.route("/")
def view_index():
    # Get count for show.
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
    # Get the page count.
    page_count = (db.get_result_set_count() + 9) // 10
    # Range limitation.
    if (page < 1 or page > page_count) and page_count:
        abort(404)
    # Generate a paginate
    pages = paginate(
        page,
        page_count,
        "/result/page/"
    )
    # Fetch results.
    results = db.get_results(10 * (page - 1), 10)
    # Make html.
    for result in results:
        result["result"]["text"] = text_to_html(result["result"]["text"])
        question_types = list(result["result"]["questions"].keys())
        for old_key in question_types:
            new_key = " ".join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', old_key).split())
            print(old_key, "to", new_key)
            result["result"]["questions"][new_key] = result["result"]["questions"].pop(old_key)
    return render_template(
        "result.html",
        results=results,
        pages=pages
    )


@app.route("/api")
def view_api():
    return render_template("api.html")


if __name__ == "__main__":
    args = parse_arguments()
    db = DB(args.host, args.port)
    app.run(host="0.0.0.0", debug=args.debug)
