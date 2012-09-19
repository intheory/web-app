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
      var video = $("#video-container")[0];
      var clickTime = video.currentTime;
      $(".click-counter").append("<img time=" + clickTime + " src='/static/imgs/hazard.png'/>");
    });

    $("#evaluate-test").click(function() {
        var clicks = $(".click-counter").children();
        var click_times = []
        clicks.each(function(index) {
            click_times.push($(clicks[index]).attr("time"));
        });   
        IT.post("/learn/hazard/evaluate", {
                 answers : JSON.stringify(click_times)
         }, true, function(response) 
         {  
            console.log("Score:"+response.score)
          });       
    });