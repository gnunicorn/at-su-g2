

$(function() {
  // Show/hide info panel
  $('.info').hover(
    function(){
      $(this).siblings('.panel').removeClass('hidden');
    },
    function(){
      $(this).siblings('.panel').addClass('hidden');
    }
    );
});
