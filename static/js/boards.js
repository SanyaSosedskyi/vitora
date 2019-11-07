$(function () {
    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("body").html(data.contentBlock);
                    $('#modal-board').modal("hide");
                } else {
                    $("#modal-board .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-board").modal("show");
            },
            success: function (data) {
                $("#modal-board .modal-content").html(data.html_form);
                }
            });
    };

  //create board
  $('.js-create-board').click(loadForm);
  $('#modal-board').on("submit", ".js-board-create-form", saveForm);

  //update board
    $('#board-table').on("click", ".js-update-board", loadForm);
    $('#modal-board').on("submit", ".js-board-update-form", saveForm);

    //delete board
    $("#board-table").on("click", ".js-delete-board", loadForm);
    $("#modal-board").on("submit", ".js-board-delete-form", saveForm);

});