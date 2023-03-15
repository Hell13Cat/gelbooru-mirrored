import traceback
from pygelbooru import Gelbooru
import PySimpleGUI as sg
import PIL
import threading
from PIL import Image
import io
import base64
import os
from PIL import Image
import requests
import json
import asyncio
import progressbar
import webbrowser
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def get_cfg(name):
    datacfg = json.load(open("config.json", "r", encoding='utf-8'))
    return datacfg[name]

def watch(filename):
    img = Image.open(filename)
    width = 600
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    img = img.resize((width, height), PIL.Image.ANTIALIAS)
    size = (width, height)
    img.save("tmp.png")
    #im = im.resize(size, resample=Image.BICUBIC)
    sg.theme('DarkPurple6')
    layout = [
        [sg.Text("Изображение сохранено")],
        [sg.Image("tmp.png", size=size, key='-IMAGE-')],
    ]
    window = sg.Window('Window Title', layout, margins=(0, 0), finalize=True)

async def get1():
    gelbooru = Gelbooru(get_cfg("api_key"), get_cfg("693972"))
    list_tags = await gelbooru.tag_list(name='dog ears')
    print(list_tags)
    list_tags = await gelbooru.tag_list(name_pattern='%small%', limit=4)
    print(list_tags)
    result = await gelbooru.random_post(tags=['cat ears', '1girl', 'cat hood', 'bell'], exclude_tags=['nude'])
    print(result)
    req = requests.get(str(result))
    cont = req.content
    open(result.filename, "wb").write(cont)
    results = await gelbooru.search_posts(tags=['dog ears', '1girl'], exclude_tags=['nude'])
    print(results)

async def gettest():
    watch("testimg.jpeg")
    fff = input("ddd")

async def get2():
    gelbooru = Gelbooru(get_cfg("api_key"), get_cfg("693972"))
    list_tags = await gelbooru.tag_list(name_pattern='%', limit=10000)
    print(len(list_tags))
    list_tagss = []
    for ii in list_tags:
        list_tagss.append(str(ii))
    list_tagss.sort()
    text = "\n".join(list_tagss)
    open("tags.txt", "w").write(text)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(get1())

def id_ready(id):
    dataf = json.load(open("data_info.json", "r", encoding='utf-8'))
    ids = dataf["id_set"]
    if id in ids:
        return 1
    else:
        return 0

def get_count():
    dataf = json.load(open("data_info.json", "r", encoding='utf-8'))
    ids = dataf["id_set"]
    return len(ids)

def add_data(data):
    resp = {}
    try:
        dataf = json.load(open("data_info.json", "r", encoding='utf-8'))
        ids = dataf["id_set"]
        ids.append(data["id"])
        dataf["id_set"] = ids
        datas = dataf["data_set"]
        tags = data["tags"].split(" ")
        dataa = {
            "id": data["id"],
            "file": data["image"],
            "data": data["created_at"],
            "rating": data["rating"],
            "source": data["source"],
            "tags": tags
        }
        datas.append(dataa)
        dataf["data_set"] = datas
        tagss = dataf["tags"]
        for ii in tags:
            if ii in tagss:
                pass
            else:
                tagss.append(ii)
        dataf["tags"] = tagss
        json.dump(dataf, open("data_info.json", "w", encoding='utf-8'), ensure_ascii=False, indent=4)
        resp["code"] = 200
        resp["text"] = "OK"
    except BaseException as e:
        resp["code"] = 602
        resp["text"] = str(e)
        resp["fulltext"] = str(traceback.format_exc)
    return resp

def save_data(url, filename):
    resp = {}
    try:
        req = requests.get(url, stream=True)
        if req.status_code == 200:
            f = open("data_img/"+filename, 'wb')
            file_size = int(req.headers['Content-Length'])
            chunk = 1
            num_bars = file_size / chunk
            bar =  progressbar.ProgressBar(maxval=num_bars)
            bar.start()
            i = 0
            for chunk in req.iter_content():
                f.write(chunk)
                bar.update(i)
                i+=1
            bar.update(num_bars)
            bar.finish()
            f.close()
        resp["code"] = req.status_code
        resp["text"] = req.reason
    except BaseException as e:
        resp["code"] = 601
        resp["text"] = str(e)
        resp["fulltext"] = str(traceback.format_exc)
    return resp


def get_data(tags, limit, pid):
    try:
        tags = tags.replace(" ", "+")
        append_auth = "&api_key="+get_cfg("api_key")+"&user_id="+get_cfg("693972")
        base_root = "https://gelbooru.com/index.php?"
        append_data = "page=dapi&s=post&q=index&json=1&limit={limit}&tags={tags}&pid={pid}".format(pid=str(pid), tags=tags, limit=str(limit))
        url_res = base_root + append_data + append_auth
        req = requests.get(url_res)
        if req.status_code == 200:
            data = req.json()
        else:
            data = {}
        data["code"] = req.status_code
        data["text"] = req.reason
        return data
    except BaseException as e:
        resp = {}
        resp["code"] = 600
        resp["text"] = str(e)
        resp["fulltext"] = str(traceback.format_exc)
        return resp


def download(datain):
    print(datain)
    data_search = json.load(open("search_data.json", "r", encoding='utf-8'))
    animated_tag = ["", " -animated", " webm", " animated", " webm"]
    rating_tag = ["", " rating:general", " rating:questionable ", " rating:explicit",]
    pages = data_search["pages"]
    limits = data_search["limits"]
    animated = data_search["animated"]
    rating = data_search["rating"]
    c_total_dw = 0
    c_total_ck = 0
    c_total_er = 0
    tags = datain["tags"]
    print("[Request] ", tags, "\nAnimated type:", animated, "\nPages:", pages, "\nLimits on page:", limits)
    for page in range(0, pages):
        data = get_data(tags+animated_tag[animated]+rating_tag[rating], limits, page)
        if data["code"] != 200:
            print("[Error] Code:", data["code"], "\nDescription:", data["text"])
            if data["code"] >= 600:
                print("----Full info----\n", data["fulltext"], "\n----Full info----")
        else:
            if "post" in data.keys():
                data = data["post"]
                count = 1
                c_page_dw = 0
                c_page_ck = 0
                c_page_er = 0
                for one_post in data:
                    print("[", tags, "|", animated, "]-[", page+1 , "/", pages, "]-[", count, "/", len(data), "]", one_post["id"], "-", one_post["image"])
                    count += 1
                    if id_ready(one_post["id"]) == 0:
                        resp = save_data(one_post["file_url"], one_post["image"])
                        if resp["code"] == 200:
                            resp = add_data(one_post)
                            if resp["code"] != 200:
                                print("[Error] Skiped\nCode:", resp["code"], "\nDescription:", resp["text"])
                                if data["code"] >= 600:
                                    print("----Full info----\n", data["fulltext"], "\n----Full info----")
                            else:
                                c_total_dw += 1
                                c_page_dw += 1
                                print("[Notify] Saved")
                        else:
                            print("[Error] Skiped\nCode:", resp["code"], "\nDescription:", resp["text"])
                            if data["code"] >= 600:
                                print("----Full info----\n", data["fulltext"], "\n----Full info----")
                            c_total_er += 1
                            c_page_er += 1
                    else:
                        c_total_ck += 1
                        c_page_ck += 1
                        print("[Notify] Skiped")
                print("[", page+1 , "/", pages, "] Current count images:", get_count(), "\nDownloads:", c_page_dw, "-", c_total_dw, "\nSkiped:", c_page_ck, "-", c_total_ck, "\nError:", c_page_er, "-", c_total_er)
            else:
                print("[Notify] Skiped page")

data_send = {"tags":"", "rating":0, "animated":0}
animated_tag = ["", " -animated", " webm", " animated", " webm"]
rating_tag = ["", " rating:general", " rating:questionable ", " rating:explicit",]


inp_tag = input(">>> ")
if inp_tag == "":
    list_dw_tags = open("list_tag.txt", "r").read().split("\n")
    page = 1
    for fff in list_dw_tags:
        inp_tag = fff
        print("[", page , "/", len(list_dw_tags), "] Current dw tags: ", fff)
        page += 1
        download({"tags":inp_tag})
else:
    download({"tags":inp_tag})