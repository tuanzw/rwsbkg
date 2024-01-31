// $("#modal").on("shown.bs.modal", function (e) {
//     console.log(e)
//     $(this).find("#id_carriers").select2({
//         dropdownParent: $(this).find(".modal-content")
//     });
// })

$("#modal").on("shown.bs.modal", function (e) {
    console.log(e)
    $(this).find("select").each(function () {
        const $p = $(this).parent();
        $(this).select2({
            dropdownParent: $p
        });
    });
});