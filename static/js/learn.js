/**
 * @fileOverview This file contains all the JavaScript functionality for the learning pages.
 * 
 */
    // =============================== Listeners =============================== //

    $("#previous-nugget-btn").live("click", function() {
        var sid = $(this).attr('sid');
        var cursor = $(this).attr('cursor');
        IT.get("/learn/get-previous-nugget", {
               sid : sid,
               cursor: cursor
        }, true, function(response) 
        {       
            var hu = $(".hero-unit");
            var parent = hu.parent();
            hu.empty().remove()
            parent.html(response.html);            
        });
    });

    $("#next-nugget-btn").live("click", function() {
        var sid = $(this).attr('sid');
        var cursor = $(this).attr('cursor');    
        IT.get("/learn/get-next-nugget", {
               sid : sid, 
               cursor: cursor
        }, true, function(response) 
        {   
            var hu = $(".hero-unit");
            var parent = hu.parent();
            hu.empty().remove()
            parent.html(response.html);
        });
    });

    $(".video-wrapper").click(function() {
      $(".click-counter").append("<img src='/static/imgs/hazard.png'/>")
    });