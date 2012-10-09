/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */
    

	$(document).ready(function () {
        if ($('.hidden').length != 0){ //if there is an unfinished test
          $(".stats-section").hide();
          $(".welcome-msg-container").fadeIn();
          $("#dim").fadeIn();
	    }
  	});

    // =============================== Listeners =============================== //
    

    //When click anywhere on page when dimmed it'll return to normal
    $("#close-welcome-msg-btn").click(function() {
      $(".welcome-msg-container").hide();
    	$(".stats-section").fadeIn();
	    $("#dim").fadeOut(2000);
      if ($("#remove-msg-checkbox").is(':checked')){
        IT.post("/dashboard/remove-msg", {
        }, true, function(response) 
        {  
          
        });
      }
	});



