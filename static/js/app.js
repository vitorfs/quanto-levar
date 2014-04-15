var LOADING = "<img src='/static/img/loading.gif' class='loading'>";

var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;
    matches = [];
    substrRegex = new RegExp(q, 'i');
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        matches.push({ value: str });
      }
    });
    cb(matches);
  };
};

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
      complete: function () {
        $("#enviar").html("Buscar");
        $("#enviar").prop("disabled", false);
        $("#cidade").prop("disabled", false);
      }
    });
    return false;
  });

  $("#conteudo").on("click", "#calculo #calcular", function () {
    return $("#dias").isValid();
  });

  $("#cidade").typeahead(
    {hint: true, highlight: true, minLength: 1},
    {name: 'cidade', displayKey: 'value', source: substringMatcher(cidades)}
    );
});