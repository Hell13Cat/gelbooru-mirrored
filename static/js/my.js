function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}
function onchange(e){
    var val = e.target.value;
    console.log(val);
    val_pars = val.split(" ");
    val_end = val_pars[val_pars.length - 1];
    url_req =  location.origin + "/autoc/" + val_end;
    resp_res = httpGet(url_req)["list"];
    var tagsac = document.getElementById("tagnameac");
    tagsac.innerHTML = '';
    resp_res.forEach(function(item, i, resp_res) {
        var add_elem = document.createElement("option");
        add_elem.value = val.replace(val_end, item+" ");
        tagsac.appendChild(add_elem);
    });
}
function search(e){
    if (e.keyCode === 13) {
        var tagsac = document.getElementById("myInput");
        var val = tagsac.value;
        replacec = 1
        while (replacec == 1) {
        val = val.replace(" ", "+");
        if(val.includes(" ")==false) {
            replacec = 0
        }
        }
            type = document.getElementById("selected-r").value;
            url_req = location.origin + "/search/" + type + "/" + val;
            resp_res = httpGet(url_req)["list"];
            console.log(resp_res);
            var imgc = document.getElementById("aniimated-thumbnials");
            imgc.innerHTML = '';
            resp_res.forEach(function(item, i, resp_res) {
            var add_elem_a = document.createElement("button");
            if (item["type"] == "i") {
                add_elem_a.setAttribute("onclick", "see_full_img('"+item["url_full"]+"', '"+item["id"]+"', '"+item["type"]+"')");
            } else {
                add_elem_a.setAttribute("onclick", "see_full_vid('"+item["url_full"]+"', '"+item["id"]+"', '"+item["type"]+"')");
            }
            add_elem_a.setAttribute("id", item["id"]);
            add_elem_a.setAttribute("class", "buttimg");
            var add_elem_img = document.createElement("img");
            add_elem_img.setAttribute("src", item["url_thumb"]);
            add_elem_img.setAttribute("loading", "lazy");
            add_elem_img.setAttribute("title", item["tags"]);
            add_elem_img.setAttribute("data-src", "/static/gif/loading.gif");
            add_elem_a.appendChild(add_elem_img);
            imgc.appendChild(add_elem_a);
        });
    }
}

function see_full_vid(url, id_button, type){
    var fulldata = document.getElementById("fulldata");
    if (fulldata != null){
        fulldata.remove();
    }
    var add_elem_br = document.createElement("br");
    var add_elem_p = document.createElement("p");
    add_elem_p.setAttribute("class", "fullimagep");
    add_elem_p.setAttribute("id", "fulldata");
    var add_elem_a = document.createElement("a");
    add_elem_a.setAttribute("href", "#"+id_button);
    var add_elem_button = document.createElement("button");
    add_elem_button.textContent = 'CLOSE';
    add_elem_button.setAttribute("class", "buttonclose");
    add_elem_button.setAttribute("onclick", "close_full()");
    var add_elem_ai = document.createElement("a");
    add_elem_ai.setAttribute("href", url);
    add_elem_ai.setAttribute("target", "_blank");
    var add_elem_img = document.createElement("video");
    add_elem_img.setAttribute("src", url);
    add_elem_img.setAttribute("class", "fullimage");
    add_elem_img.controls = true;
    add_elem_ai.append(add_elem_img)
    add_elem_p.appendChild(add_elem_button);
    add_elem_p.appendChild(add_elem_br);
    add_elem_p.appendChild(add_elem_ai);
    var targetimg = document.getElementById(id_button);
    targetimg.after(add_elem_p)
    add_elem_a.click();
}

function see_full_img(url, id_button, type){
    var fulldata = document.getElementById("fulldata");
    if (fulldata != null){
        fulldata.remove();
    }
    var add_elem_br = document.createElement("br");
    var add_elem_p = document.createElement("p");
    add_elem_p.setAttribute("class", "fullimagep");
    add_elem_p.setAttribute("id", "fulldata");
    var add_elem_a = document.createElement("a");
    add_elem_a.setAttribute("href", "#"+id_button);
    var add_elem_button = document.createElement("button");
    add_elem_button.textContent = 'CLOSE';
    add_elem_button.setAttribute("class", "buttonclose");
    add_elem_button.setAttribute("onclick", "close_full()");
    var add_elem_ai = document.createElement("a");
    add_elem_ai.setAttribute("href", url);
    add_elem_ai.setAttribute("target", "_blank");
    var add_elem_img = document.createElement("img");
    add_elem_img.setAttribute("src", url);
    add_elem_img.setAttribute("class", "fullimage");
    add_elem_ai.append(add_elem_img)
    add_elem_p.appendChild(add_elem_button);
    add_elem_p.appendChild(add_elem_br);
    add_elem_p.appendChild(add_elem_ai);
    var targetimg = document.getElementById(id_button);
    targetimg.after(add_elem_p)
    add_elem_a.click();
}
function close_full(){
    var fulldata = document.getElementById("fulldata");
    fulldata.remove();
}

function main_my(){
    var tagBox = document.getElementById("myInput");
    tagBox.addEventListener("input", onchange);
    tagBox.addEventListener("keydown", search);
}