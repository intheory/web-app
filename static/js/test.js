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
    	choices.each(function(index) {
    		if ($(this).hasClass("success")){
    			answers.push(index-1);
    		}
		});
       IT.post("/test/evaluate", {
               answers : answers,
               q_cursor: q_cursor
	   }, true, function(response) 
	   {       
	   
       });    	

    });