from io import BytesIO
from matplotlib.figure import Figure
import re

fig = Figure()
#fig.text(0, 0,r"$\frac{\vert Ax+Bx+C\vert}{\sqrt{A^2+B^2}}$")
#fig.text(0, 0,r"$\frac{\vert Ax+Bx+C\vert}{\sqrt{A^2+B^2}}$")


with BytesIO() as buf:
    fig.savefig(buf, bbox_inches="tight", pad_inches=0)
    buf.seek(0)
    with open("letest", "w+b") as file:
        file.write(buf.read())



MATH_PATTERN = re.compile(r"\<math\>.*\<\/math\>")
QUOTE_LINK_PATTERN = re.compile(r"\>\>[\d]+")
QUOTE_LINK_CROSS_PATTERN = re.compile(r"\>\>\>\/[\w]+\/[\d]+")

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

def render(text):
    raw_text = text
    text = text.__repr__()
    if (match := re.match(QUOTE_LINK_PATTERN, text)):
        start = match.start() + 2
        end = match.end()
        post_id = raw_text[start:end]

        raw_text = re.sub(QUOTE_LINK_PATTERN, text, make_link(f"comment/{post_id}"))

    if match := re.match(MATH_PATTERN, text):
        start = match.start() + 6
        end = match.end() - 11
        img_hash = save_math_png(raw_text[start:end])
        raw_text = re.sub(MATH_PATTERN, text, make_math_link(img_hash))
    return raw_text

