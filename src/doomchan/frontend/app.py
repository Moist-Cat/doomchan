from pathlib import Path
import glob
import random
from  http import HTTPStatus
import requests
import re
import json

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
from PIL import Image

app = Flask(__name__)

BASE_DIR = Path().cwd()
MEDIA_DIR = BASE_DIR / "media"
LOGOS = glob.glob(str(MEDIA_DIR) + "/*")

API_URL = Path("doomchan.com/es/api")
#Path("localhost:8000/es/api")#
def get_api_json(path, method="GET", data=None, files=None):
    append_slash = "/" if method == "POST" else ""

    if files:
        # explicitly set the fields
        # files are not send in the json
        img = files["image"]
        files = {"image": (img.filename, img.stream, img.content_type, img.headers)}

    res = requests.request(
            method,
            "https://" + str(API_URL / path) + append_slash,
            data=data,
            files=files,
            verify=False
    )
    if res.status_code <= 499:
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

@app.route("/logos/logo.png")
def logo():
    global LOGOS
    logo = random.choice(LOGOS)

    return send_file(logo)

@app.route("/thread/", methods=["POST"])
def create_thread():
    url = "thread/"
    data = request.form
    res = get_api_json(url, "POST", data, request.files)
    app.logger.info(res)
    if "pk" in res:
    #    app.session.cookies["password"] = res.json()["password"]
        return redirect(url_for("thread_view", board=data["board"],id=res["pk"]))
    return redirect(url_for("board", board=data["board"]))

@app.route("/comment/", methods=["POST"])
def create_comment():
    url = "comment/"
    data = request.form
    res = get_api_json(url, "POST", data, request.files)
    app.logger.info(res) 
    return redirect(url_for("thread_view", board=data["board"], id=data["thread"]))

@app.route("/boards/<string:board>/thread/<int:id>")
def thread_view(board, id):
    data = get_api_json(f"board/{board}")
    if data in ({'detail': 'No encontrado.'}, {'detail': 'Página inválida.'}):
        return "", HTTPStatus.NOT_FOUND
    app.logger.info(data)
    title = data["slug"]
    vname = data["verbose_name"]

    data = get_api_json(f"thread/{id}")
    return render_template(
            "4chan/thread.html",
            title=title,
            board_vname=vname,
            thread=data) 

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
