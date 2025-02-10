
$(document).ready(function() {
  function scrollToLastItem(listSelector) {
    const $list = $(listSelector);
    const $lastItem = $list.children().last(); // Get the last child element

    if ($lastItem.length > 0) { // Check if there are any items in the list
      $list.scrollTop($lastItem.offset().top - $list.offset().top + $list.scrollTop());
      // OR, a simpler but potentially less precise method:
      // $list.scrollTop($list[0].scrollHeight); // Scroll to the very bottom
    }
  }

  $('#buttonDel').click(function(){
    $('#searchInput').val('');
  });
  scrollToLastItem(".scrolleable-list");

  //  $('textarea').on('input', function() {
  //   this.style.height = 'auto'; // Reset height to recalculate
  //   this.style.height = (this.scrollHeight) + 'px'; // Set height based on content
  // });

    // Optionally trigger the event initially to set the correct height for any initial content.
    // $('textarea').trigger('input');

});