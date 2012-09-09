/**
 * @fileOverview This file contains all the JavaScript functionality for the test page.
 * 
 * @author l </a>
 */
    
    // =============================== Listeners =============================== //
    
    $("td.choice").live("click", function() {
    	$(this).parent().addClass("success");
    });

    $("a.next").live("click", function() {
    	var choices = $("tr"); //Find all the selected choices by the user
    	var answers = [];
      var cursor = $(this).attr("cursor");
      var tid = $(this).attr("tid");
    	choices.each(function(index) {
    		if ($(this).hasClass("success")){
    			answers.push(index-1);
    		}
		  });

      IT.post("/test/evaluate", {
               tid: tid,
               answers : JSON.stringify(answers),
               cursor: cursor
	     }, true, function(response) 
	     {       
          $(".hero-unit1").empty().html(response.html);
        });    	

    });