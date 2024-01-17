document.body.addEventListener("showMessage", function (evt) {
    msg_elem = document.getElementById("div_id_message");
    msg_elem.setAttribute("class", "alert alert-success");
    msg_elem.innerHTML = evt.detail.value;
});