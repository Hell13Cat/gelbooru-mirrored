from turtle import width
from urllib import response
from flask import Flask, send_file, jsonify, Markup, render_template
from PIL import Image, ImageDraw, ImageFont
import json
import io
import mimetypes
import os
import webbrowser

ip_run = "127.0.0.23"
port_run = 80

app = Flask(__name__)
global root_folder
root_folder = os.getcwd() + "\\"
print(root_folder)

@app.route("/")
def index():
    value = Markup('<strong>The HTML String</strong>')
    response = render_template("app3.html")
    return response

@app.route("/autoc/<cut_tag>")
def hentai_autoc(cut_tag):
    dataf = json.load(open(root_folder+"data_info.json", "r", encoding='utf-8'))
    tagss = dataf["tags"]
    count = 0
    list_res = []
    for ii in tagss:
        if ii.startswith(cut_tag, 0):
            count += 1
            list_res.append(ii)
    json_resp = {"count":count,"list":list_res}
    response = jsonify(json_resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/autoc/")
def hentai_autoc_m():
    dataf = json.load(open(root_folder+"data_info.json", "r", encoding='utf-8'))
    tagss = dataf["tags"]
    count = len(tagss)
    json_resp = {"count":count,"list":tagss}
    response = jsonify(json_resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/search/<types>/<tags>")
def hentai_search(types, tags):
    print(types)
    if tags[-1] == "+":
        tags = tags[:-1]
    tagsp = tags.split("+")
    dataf = json.load(open(root_folder+"data_info.json", "r", encoding='utf-8'))
    posts = dataf["data_set"]
    count = 0
    list_res = []
    for ii in posts:
        contun = 2
        for dd in tagsp:
            if dd in ii["tags"]:
                pass
            else:
                contun -= 1
        if types == "mix":
            pass
        else:
            if ii["rating"] == types:
                pass
            else:
                contun -= 1
        if contun == 2:
            if ".webm" in ii["file"] or ".mp4" in ii["file"] or ".avi" in ii["file"] or ".flv" in ii["file"]:
                typef = "v"
            else:
                typef = "i"
            res_post = {"tags":" ".join(ii["tags"]), "id":ii["id"], "type":typef, "rating":ii["rating"], "url_full":"/file/full/"+ii["file"], "url_thumb":"/file/thumb/"+ii["file"]}
            list_res.append(res_post)
            count += 1
    json_resp = {"count":count,"list":list_res}
    response = jsonify(json_resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/static/<filetype>/<filename>")
def static_a(filetype, filename):
    ext = filename.split(".")[-1]
    response = send_file(root_folder+"static/"+filetype+"/"+filename, mimetype=mimetypes.types_map['.'+ext])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/file/<filetype>/<filename>")
def hentai_img(filetype, filename):
    if filetype == "full":
        ext = filename.split(".")[-1]
        response = send_file(root_folder+"data_img/"+filename, mimetype="image/"+ext)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if filetype == "thumb":
        ext = filename.split(".")[-1]
        images = Image.open(root_folder+"data_img/"+filename)
        if images.width >= images.height:
            widtha = 250
            percent = widtha / images.width
            heighta = round(images.height * percent)
        else:
            heighta = 250
            percent = heighta / images.height
            widtha = round(images.width * percent)
        images = images.resize((widtha, heighta))
        io_data = io.BytesIO()
        if ext == "jpg":
            extf = "jpeg"
        else:
            extf = ext
        images.save(io_data, extf)
        io_data.seek(0)
        return send_file(io_data, mimetype="image/"+ext)

if __name__ == "__main__":
    app.run(ip_run, port_run, debug=True)