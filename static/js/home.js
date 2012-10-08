/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */
    

	$(document).ready(function () {
        if ($('.hidden').length != 0){ //if there is an unfinished test
          $("#dim").fadeIn();
          $(".stats-section").empty().addClass("welcome-msg").html("Copy goes here!")
      }
  	});

    // =============================== Listeners =============================== //
    
    $("#next").live("click", function() {
	if ($(this).hasClass("disabled")) return false;

	var quiz = $("#mini-quiz-box");	

	//Change question & submit the answer to the previous one	
    var qdata = $('#questions').data('questions');
    var adata = $('#answers').data('answers');	
    qdata.shift(); 
	$('#questions').data('questions', qdata);        
	var nq = qdata[0];
        if (qdata.length == 0 ){
           IT.post("/quiz/evaluate", {
               answers : String(adata)
	   }, true, function(response) 
	   {       
	       var tmpl = $("#signup-template").tmpl({score:response.score});
	       //var tmpl = $("#email-template").tmpl({score:response.score});

	       tmpl.modal().css({
		    'margin-top': function () {
		        return -($(this).height() / 2);
		    }
		})
            });
	}
	else{
		var button;
	        if (qdata.length == 1 ){
		    button = "<a id='next' class='btn btn-success btn-mini disabled'>Submit answers</a>";  
		}
		else{
   		    button = "<a id='next' class='btn btn-success btn-mini disabled'>Next Question</a>";  	
		}

		quiz.html("<h4>"+ nq.question + "</h4><ul remaining-answers="+nq.answer.length+" class='nav nav-pills nav-stacked' 			style='cursor:pointer'><li><a class='choice' ind='0'><span class='badge badge-info'>A</span> "+ nq.options[0]+"</a></li><li><a 			class='choice' ind='1'><span class='badge badge-info'>B</span> "+ nq.options[1]+"</a></li><li><a class='choice' ind='2'><span 			class='badge badge-info'>C</span> "+ nq.options[2]+"</a></li><li><a class='choice' ind='3'><span class='badge badge-info'>D</span> 			"+ nq.options[3]+"</a></li></ul>"+button);
	}
    });

    $("a.choice").live("click", function() {
	
	//Perform all animations if first time
	var quizBox = $("#mini-quiz-box");	
	if (quizBox.hasClass("undimmed")){ 
		$("#dim").fadeIn();
		var tmpl = $("#show-arrow-template").tmpl();
		$("div.columnA").after(tmpl);
		$("#mini-quiz-box").animate({
	  	   width: '+=250', left: '-150px'
		}, 400, function() {});
		quizBox.removeClass("undimmed").addClass("dimmed");
	}

	var remainingAnswers = $(this).parent().parent().attr("remaining-answers");
	if (remainingAnswers == 0 && !$(this).parent().hasClass("active")) {
		$("a.choice").parent(".active:first").removeClass("active");
		$(this).parent().addClass("active");
	    var adata = $('#answers').data('answers');
	    adata.shift(); 
	    adata.push($(this).attr("ind"));
	    $('#answers').data('answers', adata);
	    return;
	}

	if ($(this).parent().hasClass("active")){  //if this choice was clicked before unselect it
        $(this).parent().removeClass("active"); 
    	remainingAnswers = parseInt(remainingAnswers) + 1;
	    $(this).parent().parent().attr("remaining-answers", remainingAnswers);
	}	
	else{
	    $(this).parent().addClass("active");		
	    //Record answer
	    var adata = $('#answers').data('answers');
	    adata.push($(this).attr("ind"));
	    $('#answers').data('answers', adata);
	    remainingAnswers = remainingAnswers-1;
	    $(this).parent().parent().attr("remaining-answers", remainingAnswers);
	    if (remainingAnswers == 0) $("#next").removeClass("disabled").addClass("active");
	}
			
    });

    $("#mini-quiz-box").live("click", function() {return false;});
    $("#dim").css("height", $(document).height()); 

    //When click anywhere on page when dimmed it'll return to normal
    $(document).click(function() {
	if ($("#mini-quiz-box").hasClass("dimmed")){
            $("#dim").fadeOut();
            $(".arrow-container").remove(); 
	    $("#mini-quiz-box").animate({
  	       width: '-=250', left: '0px'
	    }, 400, function() {});
	    $("#mini-quiz-box").removeClass("dimmed").addClass("undimmed");
	}
    }); 
  
    $(".close").live("click", function(){
    	$('#windowTitleDialog').modal('hide');
	$("#dim").fadeOut();  
    }); 
    
    $("#get-started-btn").live("click", function() {
	var quizBox = $("#mini-quiz-box");	
	if (quizBox.hasClass("undimmed")){ 
		$("#dim").fadeIn();  
		var tmpl = $("#show-arrow-template").tmpl();
		$("div.columnA").after(tmpl);

		$("#mini-quiz-box").animate({
	  	   width: '+=250', left: '-150px'
		}, 400, function() {});
		quizBox.removeClass("undimmed").addClass("dimmed")
	}
	return false;
    });



