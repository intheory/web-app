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

    $("#section-colb-select").live("click", function() {
        //It will get all the nuggets associayed with this section
        IT.get("/admin/nuggets/get", {
                   sid : sid
        }, true, function(response) 
        {       
            console.log(response.html);
        });
    });


