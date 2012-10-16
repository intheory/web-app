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
      if (response.success){
        $("#price-tag").html("£"+response.new_price);
        $(".coupon-container").html("<p style='color:green'>Success! The new price is shown above.</p>");
      }
      else{
        $("#price-tag").html("£"+response.new_price);
        $(".coupon-container").html("<p style='color:red'>Oops! Coupon code is either invalid or expired.</p>"); 
      }
	  });

  });

  $("#pay-btn").live("click", function() {
    var code = $("#coupon-code").val();
	
	  IT.get("/payment/redirect", {
             code: code,
    }, true, function(response) 
    {   
      window.location.href = response.redirect_url;
	  });

  });

