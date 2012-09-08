/**
 * @fileOverview This file contains all the JavaScript functionality for the test page.
 * 
 * @author l </a>
 */
    
    // =============================== Listeners =============================== //
    
    $("td.choice").live("click", function() {
    	$(this).parent().addClass("success");
    });