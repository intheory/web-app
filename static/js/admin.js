/**
 * @fileOverview This file contains all the JavaScript functionality for the admin page.
 * 
 */
    
    // =============================== Listeners =============================== //
    
    $("#moderator-btn").live("click", function() {
        if ($(this).hasClass("disbaled")) return false; //if this user is a moderator do nothing
	var uid = $(this).attr("uid");
	IT.post("/admin/users/moderator", {
               uid : uid
	}, true, function(response) 
	{       
            console.log(response.moderator); 
        });
    });


