function get_map(url, map_id) {
    let base_url = window.location.origin
    url = base_url + url + map_id
    let temporary_input = document.createElement("input");
    temporary_input.value = url;
    document.body.appendChild(temporary_input);
    temporary_input.select();
    document.execCommand("copy");
    document.body.removeChild(temporary_input);
}


function delete_map(url, map_id) {
    let base_url = window.location.origin;
    let xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", base_url + url);
    xhttp.onreadystatechange = function() {
        document.getElementById(map_id).remove();
    }
    xhttp.send()
}