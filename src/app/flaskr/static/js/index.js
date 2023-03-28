let input_path;
let div_entries;
window.addEventListener("load", function (){
    input_path = document.getElementById("input-path")
    input_path.addEventListener("keydown", changeDirectory)

    div_entries = document.getElementById("entries")

    changeDirectory({key:"Enter"})
})
let path = "/"
let data = {  // pattern
    "metadata_version": 0,
    "name": "",
    "content_type": "",
    "container": 0,
    "resolution": "",
    "fps": 0,
    "audio_channels": 0,
    "ISDCF_metadata": {
        "audio_lang": "",
        "territory": "",
        "rating": "",
        "subtitle_lang": ""
    },
    "content": [
        {
            "file_name": "",
            "type": "",
            "fps": 0,
            "length": 0,
            "width": 0,
            "height": 0,
            "ratio": 0,
            "audio_length": 0,
            "audio_fps": 0
        },
        {
            "file_name": "",
            "type": "",
            "audio_length": 0,
            "audio_fps": 0
        }
        ]
}

function getPathFromElement(element) {
    let inner_html_arr = element.innerHTML.split(">")
    return inner_html_arr[inner_html_arr.length - 1].slice(1)
}

function changeDirectory(dom_object) {
    // pressed enter
    if (typeof dom_object.key !== "undefined") {
        if (dom_object.key  === "Enter") {
            path = input_path.value
        } else {
            return
        }
    } else {  // clicked
        let path_array = path.split("/")

        // pressed level up button
        if (typeof dom_object.firstChild.classList !== "undefined" && dom_object.firstChild.classList.contains("fa-level-up")) {
            path_array.pop()
        } else { // pressed folder/file name
            let position = dom_object.innerHTML.search("folder") + dom_object.innerHTML.search("video-camera")

            if (position === -2) {
                return;
            }
            path_array.push(getPathFromElement(dom_object))
        }
        path_array = path_array.filter(function (n){return n !== ""})
        path = path_array.join("/")
        path = "/" + path
        input_path.value = path
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/file_list");

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
           if (xhr.status === 200) {
               let response = JSON.parse(xhr.responseText)
               let new_inner_html = ""
               Object.keys(response).forEach(function (currentValue) {
                   let controls_html = ""
                   let itemIcon = response[currentValue]
                   if (itemIcon === "project") {
                       itemIcon = "video-camera"
                       controls_html = "<div class=\"controls\">\n" +
                           "                    <a class=\"anchor-button\" onclick=\"encode(this)\">\n" +
                           "                        <i class=\"fa fa-play\" aria-hidden=\"true\"></i>\n" +
                           "                    </a>\n" +
                           "                    <a class=\"anchor-button\" onclick=\"showInfo(this)\">\n" +
                           "                        &nbsp;<i class=\"fa fa-info\" aria-hidden=\"true\"></i>&nbsp;\n" +
                           "                    </a>\n" +
                           "                </div>\n"

                   }
                   if (itemIcon === "directory") itemIcon = "folder"

                   new_inner_html = new_inner_html +
                       "<div class=\"entry flex row\">\n" +
                       "            <a onclick=\"changeDirectory(this)\"><i class=\"fa fa-" + itemIcon + "\" aria-hidden=\"true\"></i> " + currentValue + "</a>\n" +
                       "            " + controls_html +
                       "</div>\n"

                   if (itemIcon === "video-camera") {
                       new_inner_html += "                <div class=\"info\">\n" +
                           "                </div>\n"
                   }
               })
           div_entries.innerHTML = new_inner_html}
       }};

    let formData = new FormData()
    formData.append("path", path)
    formData.append("validate_dcp_projects", "True")

    xhr.send(formData);
}

function encode(dom_object) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/encode");

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
           if (xhr.status === 200) {
               let response = JSON.parse(xhr.responseText)
               console.log(response)
       }}}

    let formData = new FormData()

    let path_array = path.split("/")
    path_array.push(getPathFromElement(dom_object.parentElement.previousElementSibling))
    path_array = path_array.filter(function (n){return n !== ""})

    let project_path = path_array.join("/")
    formData.append("project", project_path)

    xhr.send(formData);
}

function showInfo(dom_object) {
    let sessionStorageItemName = "/=" + dom_object.parentElement.previousElementSibling.textContent.slice(1)
    if (dom_object.firstElementChild.classList.contains("fa-info")) {  // is info icon - true
        let sessionStorageItemValue = sessionStorage.getItem(sessionStorageItemName)
        if (sessionStorageItemValue !== null) {  // is in storage - true
            if (dom_object.parentElement.parentElement.nextElementSibling.innerHTML.trim() === "") {  // when browser has started but div was not formed yet
                dom_object.parentElement.parentElement.nextElementSibling.innerHTML = formInfoData(JSON.parse(sessionStorageItemValue))
            }

            dom_object.parentElement.parentElement.nextElementSibling.classList.remove("hidden")
            dom_object.firstElementChild.classList.remove("fa-info")
            dom_object.firstElementChild.classList.add("fa-caret-down")
        } else {  // is in storage - false
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/project_info");

            xhr.onreadystatechange = function () {
               if (xhr.readyState === 4) {
                   if (xhr.status === 200) {
                       dom_object.parentElement.parentElement.nextElementSibling.innerHTML = formInfoData(JSON.parse(xhr.responseText))
                       sessionStorage.setItem(sessionStorageItemName, xhr.responseText)
                       dom_object.parentElement.parentElement.nextElementSibling.classList.remove("hidden")
                       dom_object.firstElementChild.classList.remove("fa-info")
                       dom_object.firstElementChild.classList.add("fa-caret-down")
               }}}

            let formData = new FormData()

            let path_array = path.split("/")
            path_array.push(getPathFromElement(dom_object.parentElement.previousElementSibling))
            path_array = path_array.filter(function (n){return n !== ""})

            let project_path = path_array.join("/")
            formData.append("project", project_path)

            xhr.send(formData);
        }
    } else {  // is info icon - false
        dom_object.parentElement.parentElement.nextElementSibling.classList.add("hidden")
        dom_object.firstElementChild.classList.remove("fa-caret-down")
        dom_object.firstElementChild.classList.add("fa-info")
    }

}

function toggleHide(dom_object) {
    console.log(dom_object.nextElementSibling)
    if (dom_object.nextElementSibling.classList.contains("hidden")) {
        dom_object.lastElementChild.classList.remove("fa-caret-right")
        dom_object.lastElementChild.classList.add("fa-caret-down")
        dom_object.nextElementSibling.classList.remove("hidden")
    } else {
        dom_object.lastElementChild.classList.remove("fa-caret-down")
        dom_object.lastElementChild.classList.add("fa-caret-right")
        dom_object.nextElementSibling.classList.add("hidden")

    }
}

function formInfoData(data) {
    if (typeof data === "string") {
        data = JSON.parse(data)
    }

    let output_div = "" +
        "                    <p><i class=\"fa fa-tag\" aria-hidden=\"true\"></i> <i class=\"key bold\">Name</i>: <i class=\"value\">" + data.name + "</i></p>\n" +
        "                    <p><i class=\"fa fa-file-video-o\" aria-hidden=\"true\"></i> <i class=\"key bold\">Content type</i>: <i class=\"value\">" + data.content_type + "</i></p>\n" +
        "                    <p><i class=\"fa fa-external-link-square\" aria-hidden=\"true\"></i> <i class=\"key bold\">Container</i>: <i class=\"value\">" + data.container + "</i></p>\n" +
        "                    <p><i class=\"fa fa-arrows\" aria-hidden=\"true\"></i> <i class=\"key bold\">Resolution</i>: <i class=\"value\">" + data.resolution + "</i></p>\n" +
        "                    <p><i class=\"fa fa-tachometer\" aria-hidden=\"true\"></i> <i class=\"key bold\">FPS</i>: <i class=\"value\">" + data.audio_channels + "</i></p>\n" +
        "                    <p><i class=\"fa fa-file-audio-o\" aria-hidden=\"true\"></i> <i class=\"key bold\">Audio channels</i>: <i class=\"value\">" + data.name + "</i></p>\n" +
        "                    <p onclick=\"toggleHide(this)\"><i class=\"fa fa-file-o\" aria-hidden=\"true\"></i> <i class=\"key bold\">ISDCF Metadata</i>  <i class=\"fa fa-caret-down\" aria-hidden=\"true\"></i></p>\n" +
        "                    <div>\n" +
        "                        <p><i class=\"key bold\">Audio Language</i>: <i class=\"value\">" + data.ISDCF_metadata.audio_lang + "</i></p>\n" +
        "                        <p><i class=\"key bold\">Territory</i>: <i class=\"value\">" + data.ISDCF_metadata.audio_lang + "</i></p>\n" +
        "                        <p><i class=\"key bold\">Rating</i>: <i class=\"value\">" + data.ISDCF_metadata.rating + "</i></p>\n"

    if (data.ISDCF_metadata.subtitle_lang !== "") {
        output_div += "                        <p><i class=\"key bold\">Subtitles Language</i>: <i class=\"value\">" + data.ISDCF_metadata.subtitle_lang + "</i></p>\n"
    }
    output_div += "                    </div>\n" +
        "                    <p onclick=\"toggleHide(this)\"><i class=\"fa fa-folder-open\" aria-hidden=\"true\"></i> <i class=\"key bold\">Content</i>  <i class=\"fa fa-caret-down\" aria-hidden=\"true\"></i></p>\n" +
        "                    <div class=\"dcp-content\">"

    for (let i = 0; i < data.content.length; i++) {
        if (data.content[i].type === "video") {
            output_div += "<p onclick=\"toggleHide(this)\"><i class=\"fa fa-film\" aria-hidden=\"true\"></i> <i class=\"value\">" + data.content[i].file_name + "</i>  <i class=\"fa fa-caret-down\" aria-hidden=\"true\"></i></p>\n" +
                "                        <div>\n" +
                "                            <p><i class=\"key bold\">Resolution</i>: <i class=\"value\">" + data.content[i].width + "x" + data.content[i].height + " (" + data.content[i].ratio +")</i></p>\n" +
                "                            <p><i class=\"key bold\">Length</i>: <i class=\"value\">" + data.content[i].length + "</i></p>\n" +
                "                            <p><i class=\"key bold\">FPS</i>: <i class=\"value\">" + data.content[i].fps + "</i></p>\n" +
                "                            <p><i class=\"key bold\">Audio Length</i>: <i class=\"value\">" + data.content[i].audio_length + "</i></p>\n" +
                "                            <p><i class=\"key bold\">Audio Sample Rate</i>: <i class=\"value\">" + (data.content[i].audio_fps / 1000) + " kHz</i></p>\n" +
                "                        </div>\n"
        } else if ((data.content[i].type === "audio")) {
            output_div += "<p onclick=\"toggleHide(this)\"><i class=\"fa fa-headphones\" aria-hidden=\"true\"></i> <i class=\"value\">" + data.content[i].file_name + "</i>  <i class=\"fa fa-caret-down\" aria-hidden=\"true\"></i></p>\n" +
                "                        <div>\n" +
                "                            <p><i class=\"key bold\">Audio Length</i>: <i class=\"value\">" + data.content[i].audio_length + "</i></p>\n" +
                "                            <p><i class=\"key bold\">Audio Sample Rate</i>: <i class=\"value\">" + (data.content[i].audio_fps / 1000) + " kHz</i></p>\n" +
                "                        </div>\n"
        } else if ((data.content[i].type === "subtitles")) {
            output_div += "<p><i class=\"fa fa-cc\" aria-hidden=\"true\"></i> <i class=\"value\">" + data.content[i].file_name + "</i></p>\n"
        }
    }
    output_div += "                    </div>\n" +
        "                    <p><i class=\"fa fa-code-fork\" aria-hidden=\"true\"></i> <i class=\"key bold\">Metadata version</i>: <i class=\"value\">" + data.metadata_version +"</i></p>\n" +
        "                </div>"

    return output_div
}
