var LOADING = "<img src='/static/img/loading.gif' class='loading'>";

$(function () {
  $("form#buscar").on("click", "#enviar", function () {
    $.ajax({
      url: '/',
      type: 'get',
      cache: false,
      beforeSend: function () {
        $("#enviar").html(LOADING);
        $("#enviar").prop("disabled", true);
        $("#cidade").prop("disabled", true);
      },
      success: function (data) {
        $("#buscar").fadeOut();
      },
      complete: function () {
        $("#enviar").html("Buscar");
        $("#enviar").prop("disabled", false);
        $("#cidade").prop("disabled", false);
      }
    });
    return false;
  });
});