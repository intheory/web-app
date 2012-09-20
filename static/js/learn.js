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

    var lastClick = 0;

    $(".video-wrapper").click(function() {
      var clicks =  $(".click-counter").children();
      if (clicks.length > 15 ){
        IT.notifier.show("Tap count cannot exceed beyond 15");
      } 
      else {
        var video = $("#video-container")[0];
        var clickTime = video.currentTime;
        
        if (clickTime - lastClick < 0.5){
          lastClick = clickTime;
          return;
        } 
        lastClick = clickTime;
        $(".click-counter").append("<img time=" + clickTime + " src='/static/imgs/hazard.png'/>");
      }
    });

    $("#evaluate-test").click(function() {
        var clicks = $(".click-counter").children();
        var click_times = [];
        var cid = $(this).attr("cid");
        clicks.each(function(index) {
            click_times.push($(clicks[index]).attr("time"));
        });   
        IT.post("/learn/hazard/evaluate", {
                 answers : JSON.stringify(click_times),
                 cid: cid
         }, true, function(response) 
         {  
            console.log("Score:"+response.score)
          });       
    });