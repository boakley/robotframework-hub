$(document).ready(function () {
  jQuery.fn.scrollTo = function(elem, speed) {
    $(this).animate({
      scrollTop: $(this).scrollTop() - $(this).offset().top + $(elem).offset().top - 10
      }, speed == undefined ? 500 : speed);
    return this;
  };

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

  var renderKeywords = function (pattern) {
    if (! _.isEmpty(pattern)) {
      $.get('/doc/search', { pattern: pattern })
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
    var pattern = state === null ? '' : state.pattern;
    renderKeywords(pattern);
    setSearchFieldValue(pattern);
  });

  var params = queryString.parse(location.search);
  if (! _.isEmpty(params.pattern)) {
    renderKeywords(params.pattern);
    setSearchFieldValue(params.pattern);
  }
  if ($('.selected').length > 0) {
    $("#right").scrollTo(".selected");
  }
});
