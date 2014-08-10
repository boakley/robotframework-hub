$(document).ready(function () {

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

  var renderKeywords = function (pattern) {
    if (! _.isEmpty(pattern)) {
      $.get('/doc/keywords', { pattern: pattern })
        .done(function (responseData) {
          $('#right').html(responseData);
        });
    } else {
      $.get('/doc/index')
        .done(function (responseData) {
          $('#right').html(responseData);
        });
    }
  }

  var refreshKeywords = function (e) {
    var pattern = $(e.target).val();
    history.pushState({ pattern: pattern }, '', '?pattern=' + pattern);
    renderKeywords(pattern);
  }

  var setSearchFieldValue = function (newValue) {
    $('#search-pattern').val(newValue);
  }

  $('#search-pattern').on('input change', _.debounce(refreshKeywords, 200));

  $(window).on('popstate', function (e) {
    var state = e.originalEvent.state;
    if (! _.isEmpty(state)) {
      renderKeywords(state.pattern);
      setSearchFieldValue(state.pattern);
    }
  });

  var params = queryString.parse(location.search);
  if (! _.isEmpty(params.pattern)) {
    renderKeywords(params.pattern)
    setSearchFieldValue(state.pattern);
  }

});
