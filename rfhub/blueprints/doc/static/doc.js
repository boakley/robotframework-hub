$(document).ready(function () {

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

  var renderKeywords = function (pattern) {
    $.get('/doc/keywords', { pattern: pattern})
      .done(function (responseData) {
        $('#right').html(responseData);
      });
  }

  var refreshKeywords = function (e) {
    pattern = $(e.target).val()
    history.pushState({}, '', '?pattern=' + pattern)
    renderKeywords(pattern);
  }

  $('#search-pattern').on('input change', _.debounce(refreshKeywords, 200));

  params = queryString.parse(location.search)
  if (params.pattern) {
    renderKeywords(params.pattern)
  }

});
