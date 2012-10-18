/**
 * @fileOverview This file contains all the JavaScript functionality for the register page.
 * 
 */

$('#registration-form').submit(function() {

	var username = $('input[name="username"]').val();
	var password = $('input[name="password"]').val();
	var email = $('input[name="email"]').val();

	IT.post("/register", {
           username : username,
           password: password,
           email:email
	}, true, function(response) 
	{       
		if (response.msg) {
			$("#registration-error-msg").html("<strong>Oops!</strong> "+response.msg).show();
		}
		else{
			window.location.href = $("#next").val();
		}
	});

  return false;
});

$('input[name="email"]').focus(function(){
	var spamMessage = $(".help-inline")
	if (spamMessage.length == 0){
		$(this).after("<span class='help-inline'><strong>We'll never spam you.</strong></span>");
	}
});

