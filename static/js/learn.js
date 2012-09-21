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
      console.log("asd")
      var clicks =  $(".click-counter").children();
      if (clicks.length > 15 ){
        IT.notifier.show("Tap count cannot exceed beyond 15");
      } 
      else {
        var video = $("#video-container")[0];
        var clickTime = video.currentTime;
        var diff = clickTime - lastClick;
        if ( diff < 0.5){ 
          lastClick = clickTime;
          return;
        } 
        lastClick = clickTime;
        $(".click-counter").append("<img time=" + lastClick + " src='/static/imgs/hazard.png' />");
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

    $(".thumbnail").click(function() {
      var clipPath = $(this).attr("clipPath");
      var videoHtml = "<div class='video-wrapper'> \
                        <video autoplay='true' id='video-container' controls='controls'>\
                          <source src='"+ clipPath +".mp4' type='video/mp4' />\
                              <source src='"+ clipPath +".webm' type='video/webm' />\
                              <object data='"+ clipPath +".mp4' width='320' height='240'>\
                            <embed src='" + clipPath +".swf' width='320' height='240' />\
                            </object> \
                        </video>\
                      </div>\
                      <div class='click-counter'>   \
                      </div>"

      $(this).animate({
           width: $(document).width()/2, 
           height: $(document).height()/2,
           zIndex:'200',
           margin:'0 auto'
      }, 600, function() {$(this).html(videoHtml)});


      $("#dim").css("height", $(document).height());
      $("#dim").fadeIn();  
    });
