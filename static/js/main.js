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

  // Hide the update button for currency change if javascript is enabled
  $('.update-currency button').addClass('hidden');

  $('select#currency').change(function(){
    var selected = $(this).find('option:selected').val();
    $('.price').each(function(){
      if ($(this).hasClass(selected)){
        $(this).removeClass('hidden');
      } else {
        $(this).addClass('hidden');
      }
    });
    $('a.order.btn').each(function(){
      if ($(this).hasClass(selected)){
        $(this).removeClass('hidden');
      } else {
        $(this).addClass('hidden');
      }
    });
  });
});
