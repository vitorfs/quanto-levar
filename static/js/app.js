var LOADING = "<img src='/static/img/loading.gif' class='loading'>";

$.fn.isValid = function () {
  var value = $(this).val();
  return !isNaN(value) && value == parseInt(value);
};

$(function () {
  $("#conteudo").on("click", "#buscar #enviar", function () {
    $.ajax({
      url: '/buscar/',
      data: $('#buscar').serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $("#enviar").html(LOADING);
        $("#enviar").prop("disabled", true);
        $("#cidade").prop("disabled", true);
      },
      success: function (data) {
        if (data != "") {
          location.href=data;
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $(".erro-busca").html(jqXHR.responseText).hide().fadeIn();
      },
      complete: function () {
        $("#enviar").html("Buscar");
        $("#enviar").prop("disabled", false);
        $("#cidade").prop("disabled", false);
      }
    });
    return false;
  });

  $("#conteudo").on("click", "#calculo #calcular", function () {
    if ($("#dias").isValid()) {
      $(".erro-dias").fadeOut();
    }
    else {
      $("#dias").focus();
      $(".erro-dias").fadeIn();
      return false;
    }
  });
});