import re
import markdown
from flask import app
from matplotlib import pyplot as plt
from matplotlib import rcParams

#rcParams["title.usetex"] = True

MATH_PATTERN = re.compile("\<math\>[\w]+\<\/math\>")

#@app.template_filter("render")
def render(text):
    text = markdown.markdown(text)
    if match := re.match(MATH_PATTERN, text):
        start = match.start() + 6
        end = match.end() - 7
        re.sub(MATH_PATTERN, text, plt.title(text[start:end]))
    return text
