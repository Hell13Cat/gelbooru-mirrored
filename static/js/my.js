function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false);
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
}


function onchange(e) {
    var val = e.target.value;
    console.log(val);
    val_pars = val.split(" ");
    val_end = val_pars[val_pars.length - 1];
    url_req = location.origin + "/autoc/" + val_end;
    resp_res = httpGet(url_req)["list"];
    var tagsac = document.getElementById("tagnameac");
    tagsac.innerHTML = '';
    resp_res.forEach(function (item, i, resp_res) {
        var add_elem = document.createElement("option");
        add_elem.value = val.replace(val_end, item + " ");
        tagsac.appendChild(add_elem);
    });
}


function search(e) {
    if (e.keyCode === 13) {
        var tagsac = document.getElementById("myInput");
        var val = tagsac.value;
        replacec = 1
        while (replacec == 1) {
            val = val.replace(" ", "+");
            if (val.includes(" ") == false) {
                replacec = 0
            }
        }
        type = document.getElementById("selected-r").value;
        url_req = location.origin + "/search/" + type + "/" + val;
        window.resp_res_main = httpGet(url_req);
        window.resp_res = resp_res_main["list"];
        var imgc = document.getElementById("aniimated-thumbnials");
        imgc.innerHTML = '';
        var paginator = document.getElementById("paginator");
        paginator.innerHTML = '';
        for (var i = 1; i <= resp_res_main["pages"]+1; i++) {
            var add_elem_paginator = document.createElement("button");
            add_elem_paginator.textContent = i;
            add_elem_paginator.setAttribute("onclick", "select_page('" + i + "')");
            add_elem_paginator.setAttribute("id", i);
            if (i==1){
                add_elem_paginator.setAttribute("class", "buttpage buttpageactive");
            } else {
                add_elem_paginator.setAttribute("class", "buttpage buttpageinactive");
            }
            paginator.appendChild(add_elem_paginator);
            console.log(i);
        }
        resp_res.forEach(function (item, i, resp_res) {
            elem_pagenum = Math.floor(i / 25) + 1
            if (elem_pagenum == 1) {
                var add_elem_a = document.createElement("button");
                add_elem_a.setAttribute("onclick", "see_full('" + item["url_full"] + "', '" + item["id"] + "', '" + item["type"] + "')");
                add_elem_a.setAttribute("id", item["id"]);
                add_elem_a.setAttribute("class", "buttimg");
                var add_elem_img = document.createElement("img");
                add_elem_img.setAttribute("src", item["url_thumb"]);
                add_elem_img.setAttribute("loading", "lazy");
                add_elem_img.setAttribute("title", item["tags"]);
                add_elem_img.setAttribute("data-src", "/static/gif/loading.gif");
                add_elem_a.appendChild(add_elem_img);
                imgc.appendChild(add_elem_a);
            }
        });
    }
}


function select_page(num) {
    var imgc = document.getElementById("aniimated-thumbnials");
    imgc.innerHTML = '';
    resp_res.forEach(function (item, i, resp_res) {
        elem_pagenum = Math.floor(i / 25) + 1
        if (elem_pagenum == num) {
            var add_elem_a = document.createElement("button");
            add_elem_a.setAttribute("onclick", "see_full('" + item["url_full"] + "', '" + item["id"] + "', '" + item["type"] + "')");
            add_elem_a.setAttribute("id", item["id"]);
            add_elem_a.setAttribute("class", "buttimg");
            var add_elem_img = document.createElement("img");
            add_elem_img.setAttribute("src", item["url_thumb"]);
            add_elem_img.setAttribute("loading", "lazy");
            add_elem_img.setAttribute("title", item["tags"]);
            add_elem_img.setAttribute("data-src", "/static/gif/loading.gif");
            add_elem_a.appendChild(add_elem_img);
            imgc.appendChild(add_elem_a);
        }
    });
    var paginator = document.getElementById("paginator");
        paginator.innerHTML = '';
        for (var i = 1; i <= resp_res_main["pages"]+1; i++) {
            var add_elem_paginator = document.createElement("button");
            add_elem_paginator.textContent = i;
            add_elem_paginator.setAttribute("onclick", "select_page('" + i + "')");
            add_elem_paginator.setAttribute("id", i);
            if (i==num){
                add_elem_paginator.setAttribute("class", "buttpage buttpageactive");
            } else {
                add_elem_paginator.setAttribute("class", "buttpage buttpageinactive");
            }
            paginator.appendChild(add_elem_paginator);
            console.log(i);
    }
}

function see_full(url, id_button, type) {
    close_full();
    var add_elem_br = document.createElement("br");
    var add_elem_p = document.createElement("p");
    add_elem_p.setAttribute("class", "fullimagep");
    add_elem_p.setAttribute("id", "fulldata");
    var add_elem_a = document.createElement("a");
    add_elem_a.setAttribute("href", "#" + id_button);
    var add_elem_button = document.createElement("button");
    add_elem_button.textContent = 'CLOSE';
    add_elem_button.setAttribute("class", "buttonfullsee");
    add_elem_button.setAttribute("onclick", "close_full()");
    var add_elem_ai = document.createElement("a");
    add_elem_ai.setAttribute("href", url);
    add_elem_ai.setAttribute("target", "_blank");
    if (type == "v") {
        var add_elem_data = document.createElement("video");
        add_elem_data.setAttribute("src", url);
        add_elem_data.setAttribute("class", "fullimage");
        add_elem_data.controls = true;
    } else {
        var add_elem_data = document.createElement("img");
        add_elem_data.setAttribute("src", url);
        add_elem_data.setAttribute("class", "fullimage");
    }
    add_elem_ai.append(add_elem_data)
    var add_elem_ag = document.createElement("a");
    add_elem_ag.setAttribute("href", 'https://gelbooru.com/index.php?page=post&s=view&id='+id_button);
    add_elem_ag.setAttribute("target", "_blank");
    var add_elem_buttong = document.createElement("button");
    add_elem_buttong.textContent = 'GELBOORU';
    add_elem_buttong.setAttribute("class", "buttonfullsee");
    add_elem_ag.append(add_elem_buttong)
    add_elem_p.appendChild(add_elem_button);
    add_elem_p.appendChild(add_elem_br);
    add_elem_p.appendChild(add_elem_ai);
    add_elem_p.appendChild(add_elem_ag);
    var targetdata = document.getElementById(id_button);
    targetdata.after(add_elem_p)
    add_elem_a.click();
}


function close_full() {
    var fulldata = document.getElementById("fulldata");
    if (fulldata != null) {
        fulldata.remove();
    }
}


function main_my() {
    var tagBox = document.getElementById("myInput");
    tagBox.addEventListener("input", onchange);
    tagBox.addEventListener("keydown", search);
}