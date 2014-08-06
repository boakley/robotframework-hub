$(document).ready(function () {

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

  $('#search-pattern').on('input change', function (e) {
    $.get('/doc/keywords', {pattern: $(e.target).val()})
      .done(function (data) {
        $('#right').html(data);
      })
  });
});
