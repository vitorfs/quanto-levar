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

  $.fn.isValid = function () {
    var value = $(this).val();
    return !isNaN(value) && value == parseInt(value);
  };

  $("#cidade").typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'states',
    displayKey: 'value',
    source: substringMatcher(states)
  });

});