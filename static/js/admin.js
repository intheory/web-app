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
        var sid = $(this).val();
        //It will get all the nuggets associayed with this section
        IT.get("/admin/nuggets/get", {
                   sid : sid
        }, true, function(response) 
        {       
            var html = '<ul>';
            for (var i = 0; i < response.nuggets.length; i++) {
                html += '<li>'+ response.nuggets[i][1] +'<input type="text" id="order-inp" nid='+ response.nuggets[i][0] +' name="order" /></li>';
            }
            html += '</ul>';
            $('.columnB').append(html);
        });
    });


    $("#save-changes-btn").live("click", function() {
        var list = $("input#order-inp");
        var ordering = {};
        for (var i = 0; i < list.length; i++) {
            var key = list.eq(i).attr("nid");
            var value = list.eq(i).val();
            ordering[key] = value;            
        }
        console.log($.parseJSON(JSON.stringify(ordering)))
        IT.post("/admin/nuggets/rearrange", {
           ordering : JSON.stringify(ordering)
        }, true, function(response) 
        {       
            console.log("Ordering changed.")
        }); 
    });