function get_map(url, map_id) {

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