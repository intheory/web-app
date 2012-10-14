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
		$("#registration-error-msg").html("<strong>Oops!</strong> "+response.msg).show()
	});

  return false;
});