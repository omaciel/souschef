jQuery(function($){
    var $rating_items = $('.rating li');
    var $rating_list = $rating_items.parent();
    var rating = /rating-(\d)/.exec($rating_list.attr('class'))[1] - 1;

    function fill_stars (number) {
        $($rating_items[number]).prevAll().andSelf().addClass('rating-active');
    }

    fill_stars(rating);

    if (!$rating_list.hasClass('rating-readonly')) {
        $rating_items.each(function(){
            $(this).hover(function(){
                $(this).prevAll().andSelf().addClass('rating-hover');
            }, function(){
                $(this).prevAll().andSelf().removeClass('rating-hover');
            });
        });
    } else {
        $rating_items.addClass('rating-readonly');
        $rating_items.click(function(e){
            e.preventDefault();
        });
    }
});