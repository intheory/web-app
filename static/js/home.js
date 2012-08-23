/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    
    
    $("a.choice").live("click", function() {
	var data = $('#questions').data('questions');
	console.log(data)
	var nq = data[1];		
	$("div.hero-unit2").html(
	"<h4>"+ nq.question + "</h4><ul class='nav nav-pills nav-stacked'><li><a class='choice'><span class='badge badge-info'>A</span> {{nq.options[0]}}</a></li><li><a class='choice'><span class='badge badge-info'>B</span> {{nq.options[1]}}</a></li><li><a class='choice'><span class='badge badge-info'>C</span> {{nq.options[2]}}</a></li><li><a class='choice'><span class='badge badge-info'>D</span> {{nq.options[3]}}</a></li></ul>"	
	);
    });
    
    



