	var navBtns = $(".nav.nav-pills").children();
    navBtns.each(function(index) {
      if ($(this).hasClass("active")){
        $(this).removeClass("active");
      }
    });    