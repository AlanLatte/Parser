$(document).ready(function(){
  var $input = $("#app input"),
      $appendHere = $(".tagHere"),
      oldKey = 0, newKey,
      TABKEY = 9
      data = [];
  $input.focus();

  $input.keydown(function(e){

    if(e.keyCode == TABKEY) {
      if(e.preventDefault) {
        e.preventDefault();
        if($(this).val() == '' || $(this).val() == ' ') {
          return false;
        }
        data.push($(this).val());
        addTag($(this));

      }
      return false;
    }

    if($(this).val() == '' && e.keyCode === 8) {
      $(".tag:last-child").remove();
    }

  })
  $("#commit").on("click", function() {
      var js_data = JSON.stringify(data);
      $.ajax({
          url: '/search',
          type : 'post',
          contentType: 'application/json',
          dataType : 'json',
          data : js_data
      }).done(function(result) {
          console.log(result);
          $("#data").html(result);
      }).fail(function(jqXHR, textStatus, errorThrown) {
          console.log("fail: ",textStatus, errorThrown);
      });
  });
  function addTag(element) {
    var $tag = $("<div />"), $a = $("<a href='' />"), $span = $("<span />");
    $tag.addClass('tag');
    $('<i class="fa fa-times" aria-hidden="true"></i>').appendTo($a);
    $span.text($(element).val());
    $a.bind('click', function(){
      $(this).parent().remove();
      $(this).unbind('click');
    });
    $a.appendTo($tag);
    $span.appendTo($tag);
    $tag.appendTo($appendHere);
    $(element).val('');
  }
});
