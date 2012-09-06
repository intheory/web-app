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
            $("#nugget-title-container").html("<p><font color='#FFFFFF'><b>"+  response.nugget_title +" </b></font></p>");
            $("#nugget-content-container").html(response.nugget_content);
            $(this).attr("cursor", response.new_cursor);            
            $("#next-nugget-btn").attr("cursor", response.new_cursor)    
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
            $("#nugget-title-container").html("<p><font color='#FFFFFF'><b>"+  response.nugget_title +" </b></font></p>");
            $("#nugget-content-container").html(response.nugget_content);
            $(this).attr("cursor", response.new_cursor);           
            $("#previous-nugget-btn").attr("cursor", response.new_cursor)     
        });
    });