import argparse
from flask import Flask
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


@app.route('/')
def index():
    return "{} texts are waiting for process &" \
           " {} results are waiting for export.".format(
        db.get_text_queue_count(),
        db.get_result_set_count()
    )


if __name__ == "__main__":
    args = parse_arguments()
    db = DB(args.host, args.port)
    app.run(host="0.0.0.0", debug=args.debug)
