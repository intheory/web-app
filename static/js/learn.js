/**
 * @fileOverview This file contains all the JavaScript functionality for the learning pages.
 * 
 */
    // =============================== Listeners =============================== //

    $("#previous-nugget-btn").live("click", function() {
        var pnid = $(this).attr('pnid');
        IT.get("/learn/get-previous-nugget", {
               pnid : pnid
        }, true, function(response) 
        {       
            $("#nugget-title-container").html("<p><font color='#FFFFFF'><b>"+  response.nugget_title +" </b></font></p>");
            $("#nugget-content-container").html(response.nugget_title);
            $("#previous-nugget-btn").attr("pnid", response.nugget_previous);
            $("#next-nugget-btn").attr("nnid", response.nugget_next);
        });
    });

    $("#next-nugget-btn").live("click", function() {
        var nnid = $(this).attr('nnid');
        IT.get("/learn/get-next-nugget", {
               nnid : nnid
        }, true, function(response) 
        {       
            $("#nugget-title-container").html("<p><font color='#FFFFFF'><b>"+  response.nugget_title +" </b></font></p>");
            $("#nugget-content-container").html(response.nugget_title);
            $("#previous-nugget-btn").attr("pnid", response.nugget_previous);
            $("#next-nugget-btn").attr("nnid", response.nugget_next);
        });
    });