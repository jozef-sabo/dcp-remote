let inputPath;
let entries;
window.addEventListener("load", function (){
    inputPath = document.getElementById("input-path")
    inputPath.addEventListener("keydown", changeDirectory)

    entries = document.getElementById("entries")

    changeDirectory({key:"Enter"})
})
let path = "/"

function changeDirectory(dom_object) {
    // pressed enter
    if (typeof dom_object.key !== "undefined") {
        if (dom_object.key  === "Enter") {
            path = inputPath.value
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
            let inner_html_arr = dom_object.innerHTML.split(">")

            if (position === -2) {
                return;
            }
            path_array.push(inner_html_arr[inner_html_arr.length - 1].slice(1))
        }
        path_array = path_array.filter(function (n){return n !== ""})
        path = path_array.join("/")
        path = "/" + path
        inputPath.value = path
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
           entries.innerHTML = new_inner_html}
       }};

    let formData = new FormData()
    formData.append("path", path)
    formData.append("validate_dcp_projects", "True")

    xhr.send(formData);
}

function encode(dom_object) {
    console.log(dom_object.parentElement.previousElementSibling.innerHTML)
}

function showInfo(dom_object) {
    console.log(dom_object.parentElement.previousElementSibling.innerHTML)
}


