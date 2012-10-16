/**
 * @fileOverview This file contains all the JavaScript functionality for the payment page.
 * 
 */

 $("#show-coupon-btn").click(function() {
 	$(".input-append").toggle();
  });

  $("#redeem-btn").live("click", function() {
    var code = $("#coupon-code").val();
	
	IT.get("/payment/redeem-coupon", {
             code: code,
    }, true, function(response) 
    {   
    	$("#price-tag").html("£"+response.new_price);
	});

  });

  $("#pay-btn").live("click", function() {
    var code = $("#coupon-code").val();
	
	IT.get("/payment/redirect", {
             code: code,
    }, true, function(response) 
    {   
    	$("#price-tag").html("£"+response.new_price);
	});

  });

