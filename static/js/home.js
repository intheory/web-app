/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */
    
    // =============================== Listeners =============================== //
         
    $("a.choice").live("click", function() {
	$("#dim").fadeIn();
	if ($(this).parent().hasClass("active")) return; //if this choice was clicked before DO NOTHING
	
	var remainingAnswers = $(this).parent().parent().attr("remaining-answers")

	//Record answer
        var adata = $('#answers').data('answers');
        adata.push($(this).attr("ind"));
	$('#answers').data('answers', adata);
	remainingAnswers = remainingAnswers-1;
	$(this).parent().parent().attr("remaining-answers", remainingAnswers)
	
	//Change question	

	//if this is a multi-answer question do not change	
	if (remainingAnswers != 0){
	    $(this).parent().addClass("active")		
	}
	else{	
  	    var qdata = $('#questions').data('questions');
	    qdata.shift(); 
	    var nq = qdata[0];
	    if (qdata.length == 0 ){
	        IT.post("/quiz/evaluate", {
                    answers : String(adata)
		}, true, function(response) 
		{       
			var tmpl = $("#signup-template").tmpl({score:response.score});

			tmpl.modal().css({
			    'margin-top': function () {
			        return -($(this).height() / 2);
			    }
			})
	        });
	    }else{	
		$('#questions').data('questions', qdata);
		$("div.hero-unit2").html("<h4>"+ nq.question + "</h4><ul remaining-answers="+nq.answer.length+" class='nav nav-pills nav-stacked' style='cursor:pointer'><li><a class='choice' ind='0'><span class='badge badge-info'>A</span> "+ nq.options[0]+"</a></li><li><a class='choice' ind='1'><span class='badge badge-info'>B</span> "+ nq.options[1]+"</a></li><li><a class='choice' ind='2'><span class='badge badge-info'>C</span> "+ nq.options[2]+"</a></li><li><a class='choice' ind='3'><span class='badge badge-info'>D</span> "+ nq.options[3]+"</a></li></ul>"	
		);
	    }
	}
	
    });

    $("#dim").css("height", $(document).height()); 

    $(".close").live("click", function(){
    	$('#windowTitleDialog').modal('hide');
    }); 
    
    $("#get-started-btn").live("click", function() {
	$("#dim").fadeIn();  
    });



