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

  function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
  }

  function renderKeywords(pattern) {
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

  function refreshKeywords(e) {
    var pattern = $(e.target).val();
    var url = '/doc/keywords/';
    if (!_.isEmpty(pattern)) {
      url = url + '?pattern=' + pattern;
    }
    history.pushState({ pattern: pattern }, '', url);
    renderKeywords(pattern);
  }

  function setSearchFieldValue(newValue) {
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
