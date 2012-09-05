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
            console.log(response.nugget_title);
            //TODO: Replace old nugget with new
        });
    });