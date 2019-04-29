$(document).ready(function(){
  var $input          = $("#app input"),
      $appendHere     = $(".tagHere"),
      oldKey          = 0, newKey,
      TABKEY          = 9,
      ENTERKEY        = 13,
      data            = [];
  $input.focus();

  $input.keydown(function(e){

    if(e.keyCode == TABKEY) {
      if(e.preventDefault) {
        e.preventDefault();
        if($(this).val() == '' || $(this).val() == ' ') {
          false;
        }
        data.push($(this).val());
        addTag($(this));

      }
      return false;
    }

    if($(this).val() == '' && e.keyCode === 8) {
      $(".tag:last-child").remove();
    }

    if(e.keyCode == ENTERKEY) {
      function unique(arr) {
        var obj = {};
        for (var i = 0; i < arr.length; i++) {
          var str = arr[i];
          obj[str] = true;
        }
        return Object.keys(obj);
      }
      var js_data = JSON.stringify(unique(data));
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

    }

  })
  function addTag(element) {
    var $tag = $("<div />"), $a = $("<a />"), $span = $("<span />");
    $tag.addClass('tag');
    $('<i class="fa fa-times" aria-hidden="true"></i>').appendTo($a);
    $span.text($(element).val());
    $a.bind('click', function(){
      // TODO: Удаление объектов из массива
      // var index = data.indexOf($(element));
      // if (index > -1) {
      //   data.splice(index, 1);
      // }
      $(this).parent().remove();
      $(this).unbind('click');

      $input.focus();
    });
    $a.appendTo($tag);
    $span.appendTo($tag);
    $tag.appendTo($appendHere);
    $(element).val('');
  }
});
