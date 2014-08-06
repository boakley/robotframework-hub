$(document).ready(function () {

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

  var fetchKeywords = function (e) {
    var postData = { pattern: $(e.target).val() }
    $.get('/doc/keywords', postData)
      .done(function (responseData) {
        $('#right').html(responseData);
      });
    }

  $('#search-pattern').on('input change', _.debounce(fetchKeywords, 200));

});
