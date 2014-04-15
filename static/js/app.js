var LOADING = "<img src='/static/img/loading.gif' class='loading'>";

$(function () {
  $(".titulo").click(function () {
    $.ajax({
      url: '/buscar/',
      type: 'get',
      cache: false,
      success: function (data) {
        $("#conteudo").fadeOut(400, function () {
          $("#conteudo").hide().html(data).fadeIn();
          $("title").text("Quanto Levar?");
          window.history.pushState("", "", "/");
        });
      }
    });
  });

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
        $("#buscar").fadeOut(400, function () {
          $("#conteudo").hide().html(data).fadeIn();
          var slug = "/" + $("#slug").val() + "/";
          window.history.pushState("", "", slug);
          var titulo_pagina = $("#titulo-pagina").val();
          $("title").text(titulo_pagina);
        });
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
    $.ajax({
      url: '/calculo/',
      data: $("#calculo").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $("#calcular").html(LOADING);
        $("#calcular").prop("disabled", true);
      },
      success: function (data) {
        $("#calculo").fadeOut(400, function () {
          $("#conteudo .container").html(data).fadeIn();
        });
      },
      complete: function () {
        $("#calcular").html("Calcular");
        $("#calcular").prop("disabled", false);
      }
    });
    return false;
  });

  $("#conteudo").on("click", "#calculo #calcular", function () {
    return $("#dias").isValid();
  });

  $("#conteudo").on("click", "#voltar", function () {
    $.ajax({
      url: '/buscar/',
      data: $('#voltar-cidade').serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("#resultado-calculo").fadeOut(400, function () {
          $("#conteudo").html(data).fadeIn();
        });
      }
    });
    return false;
  });

  $.fn.isValid = function () {
    var value = $(this).val();
    return !isNaN(value) && value == parseInt(value);
  };

});