function find_card() {
  var $this = $(this);
  var filename = "LO-" + $('#cardno').val();
  var info_path = "/card_db/info/" + filename + ".json";
  $.get(info_path, function(data) {
    $('#output-desc').text(data['desc']);
    var qna_list = data['qna'];
    var t=qna_list.join("<br/>");
    $('#output-qna').html(t);
  }, 'json');
  var img_path = "/card_db/img/" + filename + ".png";
  $('#card_img').attr('src', img_path);
}

$(document).ready(function() {
  $('#addon2').on('click', function() {
    find_card()
  });
})

$(document).keypress(function(e) {
  if(e.which == 13) {
    find_card()
  }
});
