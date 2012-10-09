/**
 * @fileOverview This file contains all the JavaScript functionality for the test page.
 * 
 * @author l </a>
 */

// =============================== Delete test on unload code =============================== //

$(window).bind('beforeunload', function() {
    if ($(".countdowntime").length != 0){  //TODO: find a better way to distinguish pracrise tests and mock tests pages
      return 'If you leave now you will lose all the progress in this test.' ;
    }
});

$(window).unload( function () { 
  var tid = $(".next").attr("tid");
  IT.post("/test/delete", {
             tid: tid,
         }, true, function(response) 
         {  

         }, true, true, false
  );  
  return false;
});

// =============================== Test timer code =============================== //

var countdownTimer, countdownCurrent = 3.42 * 100000;
$(document).ready(function() {
  countdownTimer = $.timer(function() {
    var min = parseInt(countdownCurrent/6000);
    var sec = parseInt(countdownCurrent/100)-(min*60);
    var output = "00"; if(min > 0) {output = pad(min,2);}
    $('.countdowntime').html("<h3>" + output+":"+pad(sec,2) + "</h3>" );
    if(countdownCurrent == 0) {
      countdownTimer.stop();
      alert('Example 2: Countdown timer complete!');
      countdownReset();
    } else {
      countdownCurrent-=7;
      if(countdownCurrent < 0) {countdownCurrent=0;}
    }
  }, 70, true);
});

function countdownReset() {
  var newCount = parseInt($('input[name=startTime]').val())*100;
  if(newCount > 0) {countdownCurrent = newCount;}
  countdownTimer.stop().once();
}

// Padding function
function pad(number, length) {
  var str = '' + number;
  while (str.length < length) {str = '0' + str;}
  return str;
}

// =============================== Unfinished test code =============================== //
  $(document).ready(function () {
        if ($('.hidden').length != 0){ //if there is an unfinished test
          $("#dim").fadeIn();
          var tmpl = $("#existing-test-info-template").tmpl();
          IT.popup.show(tmpl);
      }
  });

 $(".notify-blurb-close-btn, #carry-on-btn").live("click", function() {
    $("#dim").fadeOut(1500);
    IT.popup.close();
 });

  $("#create-new-btn").live("click", function() {
    var tid = $("li.next").attr("tid");
    IT.get("/test/get-new", {
                 tid: tid,
         }, true, function(response) 
         {  
            $(".landing").empty().html(response.html);
            $("#dim").fadeOut(1500);
            IT.popup.close();
          });
  });


    // =============================== Listeners =============================== //

    $("td.choice").live("click", function() {
      var choiceRow = $(this).parent();
      var remainingAnswers = parseInt($(".next").attr("remaining-answers"));

      if (choiceRow.hasClass("success")){
        choiceRow.removeClass("success");
        $(".next").attr("remaining-answers", remainingAnswers+1);
      }
      else{
        if (remainingAnswers==0){
          $("td.choice").parent(".success").first().removeClass("success");
          choiceRow.addClass("success");        
        }
        else{
          choiceRow.addClass("success");        
          $(".next").attr("remaining-answers", remainingAnswers-1);
        }
      }
    });

    $("li.next-after-wrong-answer").live("click", function() {
        var tid = $(this).attr("tid");
        IT.get("/test/get-next-after-wrong", {
                 tid: tid
        }, true, function(response) 
        {  
          $(".landing").empty().html(response.html);
        });
    });

    $("li.next").live("click", function() {
    	var choices = $("tr"); //Find all the selected choices by the user
    	var answers = [];
      var cursor = $(this).attr("cursor");
      var tid = $(this).attr("tid");
    	var remainingAnswers = $(this).attr("remaining-answers");
      choices.each(function(index) {
    		if ($(this).hasClass("success")){
    			answers.push(index-1);
    		}
		  });

      if (remainingAnswers==0){
        IT.get("/test/get-next", {
                 tid: tid,
                 answers : JSON.stringify(answers),
                 cursor: cursor
  	     }, true, function(response) 
  	     {  
           if (response.correct){
             $(".landing").empty().html(response.html);
           }
           else{
             $(".maincontent").empty().html(response.html);
             //Color transition
             $(".maincontent").css({ backgroundColor: "#B94A48" });
             $(".maincontent").animate({ backgroundColor: "#F2DEDE" }, 1500);
           }
           IT.popup.close();
          });    	
      }
      else{
        var variableText = "answers."
        if (remainingAnswers==1) variableText="answer."
        IT.popup.show("Please mark "+remainingAnswers+" more "+ variableText)
      }

    });

    $("li.previous").live("click", function() {
        var cursor = $(this).attr("cursor"), 
            tid = $(this).attr("tid");

        IT.get("/test/get-previous", {
                 tid: tid,
                 cursor: cursor
         }, true, function(response) 
         {  
            $(".landing").empty().html(response.html);
          }); 
    });    

    $("li.explain").live("click", function() {
      $(".question").css({"display":"none"});
      $(".explanation").css({"display":"block"});          
    });    


    $("li.return").live("click", function() {
      $(".explanation").css({"display":"none"});
      $(".question").css({"display":"block"});          
    });    
