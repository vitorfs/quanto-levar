var LOADING = "<img src='/static/img/loading.gif' class='loading'>";

$(function () {
  $("#cidade").click(function () {
    $(this).html(LOADING);
    return false;
  });
});