$(document).ready(function () {
  "use strict";

  $('label.tree-toggler').click(function () {
      $(this).parent().children('ul.tree').toggle(200);
  });

});
