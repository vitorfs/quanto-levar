var LOADING = "<img src='/static/img/loading.gif'>";

$(function () {
  $("#cidade").click(function () {
    $(this).html(LOADING);
    return false;
  });
});