from io import BytesIO
import re
from pathlib import Path
import glob
import random
from  http import HTTPStatus
import requests
import re
import json

#import markdown
from matplotlib.figure import Figure
from PIL import Image
from flask import (
        Flask,
        render_template,
        send_file,
        request,
        url_for,
        redirect,
        abort,
        Response
)

#rcParams["title.usetex"] = True

# globals
MATH_PATTERN = re.compile(r"<math>.*</math>")
QUOTE_LINK_PATTERN = re.compile(r"\>\>[\d]+")
QUOTE_LINK_CROSS_PATTERN = re.compile(r"\>\>\>\/[\w]+\/[\d]+")

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
MEDIA_DIR = BASE_DIR / "media"
LOGOS = glob.glob(str(MEDIA_DIR) + "/*")
MATH_DIR = BASE_DIR.parent / "static" / "math" if not app.debug else BASE_DIR / "static" / "math"

if app.debug:
    API_URL = "http://localhost:8000/es/api/"
else:
    API_URL = "https://doomchan.com/es/api/"

# filters
def make_link(path):
    return f"<a id=\"quote_link\" href={path}>>>>{path}</a>"

def make_math_link(img_path):
    return f"<img src=\"/static/math/{img_path}\">"

def save_math_png(string):
    fig = Figure()
    fig.text(0, 0, string)

    img_hash = str(abs(hash(string))) + ".png"
    with BytesIO() as buf:
        fig.savefig(buf, fomat="png", bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        with open(MATH_DIR / img_hash, "w+b") as file:
            file.write(buf.read())
    return img_hash

@app.template_filter("render")
def render(text):
    if (match := re.search(QUOTE_LINK_PATTERN, text)):
        start = match.start() + 2
        end = match.end()
        post_id = text[start:end]

        app.logger.info("rendering %s", post_id)

        text = re.sub(QUOTE_LINK_PATTERN, make_link(f"comment/{post_id}"), text)

    if match := re.search(MATH_PATTERN, text):
        app.logger.info("MATH_DETECTED")
        img_hash = save_math_png(match.string[match.start() + 6: match.end() - 7])
        app.logger.info(text)
        text = re.sub(MATH_PATTERN, make_math_link(img_hash), text)
        app.logger.info(text)
    return text

# utils
def get_api_json(path, method="GET", data=None, files=None):
    append_slash = "/" if method == "POST" else ""

    if files:
        # explicitly set the fields
        # files are not send in the json
        img = files["image"]
        files = {"image": (img.filename, img.stream, img.content_type, img.headers)}

    res = requests.request(
            method,
            API_URL + path + append_slash,
            data=data,
            files=files,
            verify=False
    )
    if res.status_code <= 499 and res.status_code != 404:
        js_res = res.json()
        if "detail" in js_res:
            app.logger.error({"error": js_res["detail"], "data": data, "files": files})
        else:
             return js_res
    try:
        abort(
             Response(
                 response=res.json()["detail"] if "detail" in res.json() else None,
                 status=res.status_code
            )
        )
    except json.decoder.JSONDecodeError:
        abort(Response(status=res.status_code))
       

def get_page_num(url):
    match = re.search("page=[1-9][0]?", url)
    clean_str = '1'
    if match:
        clean_str = re.sub("=", "", match.string[match.end() - 2: match.end()])
    return clean_str

# views
@app.route("/logos/logo.png")
def logo():
    global LOGOS
    logo = random.choice(LOGOS)

    return send_file(logo)

@app.route("/thread/", methods=["POST"])
def create_thread():
    url = "thread"
    data = request.form
    res = get_api_json(url, "POST", data, request.files)
    app.logger.info(res)
    if "pk" in res:
    #    app.session.cookies["password"] = res.json()["password"]
        return redirect(url_for("thread_view", board=data["board"],id=res["pk"]))
    return redirect(url_for("board", board=data["board"]))

@app.route("/comment/", methods=["POST"])
def create_comment():
    url = "comment"
    data = request.form
    res = get_api_json(url, "POST", data, request.files)
    app.logger.info(res) 
    return redirect(url_for("thread_view", board=data["board"], id=data["thread"]))

@app.route("/boards/<string:board>/thread/<int:id>")
def thread_view(board, id):
    board_data = get_api_json(f"board/{board}")
    if board_data in ({'detail': 'No encontrado.'}, {'detail': 'Página inválida.'}):
        return "", HTTPStatus.NOT_FOUND
    title = board_data["slug"]
    vname = board_data["verbose_name"]

    thread_data = get_api_json(f"thread/{id}")
    app.logger.info(thread_data)
    return render_template(
            "4chan/thread.html",
            title=title,
            board_vname=vname,
            thread=thread_data)

@app.route("/<string:board>/")
@app.route("/<string:board>/<int:page>")
@app.route("/boards/<string:board>")
@app.route("/boards/<string:board>/<int:page>")
@app.route("/boards/<string:board>/catalog")
@app.route("/boards/<string:board>/catalog?search=<string:query>")
@app.route("/boards/<string:board>/catalog/<int:page>")
def board(board, page=1, query=""):
    data = get_api_json(f"board/{board}?page={page}&search={query}")
    if data in ({'detail': 'No encontrado.'}, {'detail': 'Página inválida.'}):
        return "", HTTPStatus.NOT_FOUND
    app.logger.info(data)
    title = data["slug"]
    vname = data["verbose_name"]

    threads = data["threads"]

    pages = threads["count"] // 10
    nxt = get_page_num(threads["next"]) if threads["next"] else None
    prev = get_page_num(threads["previous"]) if threads["previous"] else None

    raw_threads = threads["results"]
    app.logger.info(raw_threads)

    return render_template(
            "4chan/catalog.html",
            page=page,
            title=board,
            board_vname=vname,
            pages=pages,
            nxt=nxt,
            prev=prev,
            threads=raw_threads
    )

if __name__ == "__main__":
    app.run(port=5000)
