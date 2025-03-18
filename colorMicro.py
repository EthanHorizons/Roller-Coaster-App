from flask import Flask, jsonify

import random
import colorsys
from collections import OrderedDict

app = Flask(__name__)
url = "http://localhost:6000/color"
headers = {
    'Content-Type': "application/ld+json"
}
def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return int(r * 255), int(g * 255), int(b * 255)

def hsl_to_hex(h, s, l):
    r, g, b = hsl_to_rgb(h, s, l)
    return f"#{r:02x}{g:02x}{b:02x}"

def genColors():
    #generate starter color
    hue = random.randint(0,360)
    sat = random.randint(60,100)
    light = random.randint(40,60)
    colors = OrderedDict()
    #make first three colors
    colors["primeColor"] = hsl_to_hex((hue + 0*30) % 360, sat, light)
    colors["secColor"] = hsl_to_hex((hue + 1*30) % 360, sat, light)
    colors["backColor"] = hsl_to_hex((hue + 2*30) % 360, sat, light)
    #make complementry for text and footer
    comHue = (hue + 180) % 360
    colors["textColor"] = hsl_to_hex(comHue, sat, light)
    highHue = (comHue + 25) % 360
    colors["highColor"] = hsl_to_hex(highHue, sat, light)
    colors["footer"] = colors["textColor"]

    print(colors)
    return colors


@app.route('/color', methods=['GET'])
def color():
    themeData = genColors();
    return jsonify(themeData)

if __name__ == '__main__':
    app.run(port=5500)  

