/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
        
    $("a.choice").live("click", function() {
	//Record answer
        var adata = $('#answers').data('answers');
        adata.push($(this).attr("ind"));
	$('#answers').data('answers', adata);
	
	//Change question	
	var qdata = $('#questions').data('questions');
	qdata.shift(); 
	var nq = qdata[0];
	if (qdata.length == 0 ){
	        IT.post("/quiz/evaluate", {
                    answers : String(adata)
		}, true, function(response) 
		{
			$("div.hero-unit2").html("Hey, loser! Your score is "+response.score)
	        });
	}else{	
		$('#questions').data('questions', qdata);
		$("div.hero-unit2").html(
		"<h4>"+ nq.question + "</h4><ul class='nav nav-pills nav-stacked' style='cursor:pointer'><li><a class='choice' ind='0'><span class='badge badge-info'>A</span>"+ nq.options[0]+"</a></li><li><a class='choice' ind='1'><span class='badge badge-info'>B</span>"+ nq.options[1]+"</a></li><li><a class='choice' ind='2'><span class='badge badge-info'>C</span>"+ nq.options[2]+"</a></li><li><a class='choice' ind='3'><span class='badge badge-info'>D</span> "+ nq.options[3]+"</a></li></ul>"	
		);
	}
	
    });
    



