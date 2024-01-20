;(function (){
    const modal = new bootstrap.Modal(document.getElementById("modal"))

    htmx.on("htmx:afterSwap", (e) => {
        console.log(e.detail.target.id)
        if (e.detail.target.id == "dialog") {
            modal.show()
        }
    })
    htmx.on("htmx:beforeSwap", (e) => {
        console.log(e)
        if (e.detail.target.id == "table_id_carrier") {
            modal.hide()
        }
    })
    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = ""
    })
    htmx.on("on-success", () => {
        console.log("on-success")
        // modal.hide()
    })
    htmx.on("frm-has-errors", () => {
        console.log("frm-has-errors")
        document.getElementById("btn-id-save").disabled = true
    })
    htmx.on("frm-no-errors", () => {
        console.log("frm-no-errors")
        document.getElementById("btn-id-save").disabled =false
    })
})()