;(function(){
    htmx.on("htmx:confirm", (e) => {
        console.log(e)
        e.preventDefault()
        Swal.fire({
            title: "Confirm?",
            // text: `Do you want to delete: ${e.detail.question}`,
            text: e.detail.question,
            showCancelButton: true,
            confirmButtonText: "Yes"
        }).then(function (result) {
            if (result.isConfirmed) e.detail.issueRequest(true) // use true to skip window.confirm
        })
    })
})()