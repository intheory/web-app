
$(document).ready(function() {
    $("#dim").css("height", $(document).height()).fadeIn(); 
    $('#video-container').bind('ended',onEnd);  
});

function onEnd(){
    var clicks = $(".click-counter").children(),
        click_times = [],
        cid = $("video#video-container").attr("cid");

    if (cid === "intro") {
      window.location.href = "/learn/hazardboard" ;
      return
    }

    clicks.each(function(index) {
        click_times.push($(clicks[index]).attr("time"));
    });   
    IT.post("/learn/hazardboard/evaluate", {
             answers : JSON.stringify(click_times),
             cid: cid
     }, true, function(response) 
     {  
        $(".landing").empty().html(response.html);
        $("#dim").fadeOut();
      });       
}

    var lastClick = 0;

    $(".video-wrapper").live("click", function() {
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