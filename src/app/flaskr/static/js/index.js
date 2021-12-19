let input_path;
let div_entries;
let div_info;
window.addEventListener("load", function (){
    input_path = document.getElementById("input-path")
    input_path.addEventListener("keydown", changeDirectory)

    div_entries = document.getElementById("entries")

    div_info = document.getElementById("info")

    changeDirectory({key:"Enter"})
})
let path = "/"

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
                           "                        <i class=\"fa fa-info\" aria-hidden=\"true\"></i>\n" +
                           "                    </a>\n" +
                           "                </div>\n"
                   }
                   if (itemIcon === "directory") itemIcon = "folder"

                   new_inner_html = new_inner_html +
                       "<div class=\"entry flex row\">\n" +
                       "            <a onclick=\"changeDirectory(this)\"><i class=\"fa fa-" + itemIcon + "\" aria-hidden=\"true\"></i> " + currentValue + "</a>\n" +
                       "            " + controls_html +
                       "</div>\n"
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
               div_info.innerText = xhr.responseText
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
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/project_info");

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
           if (xhr.status === 200) {
               let response = JSON.parse(xhr.responseText)
               console.log(response)
               div_info.innerText = xhr.responseText
       }}}

    let formData = new FormData()

    let path_array = path.split("/")
    path_array.push(getPathFromElement(dom_object.parentElement.previousElementSibling))
    path_array = path_array.filter(function (n){return n !== ""})

    let project_path = path_array.join("/")
    formData.append("project", project_path)

    xhr.send(formData);
}


