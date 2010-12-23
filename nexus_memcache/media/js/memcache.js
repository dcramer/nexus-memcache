$(function(){
    $('.toggle').click(function(){
        if ($(this).text() == 'Expand') {
            $(this).siblings('.more').css('display', 'block');
            $(this).text('Collapse');
        } else {
            $(this).siblings('.more').css('display', 'none');
            $(this).text('Expand');
        }
    })
});