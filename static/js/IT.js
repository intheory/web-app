/**
 * @fileOverview This file contains the core JavaScript functionality of the site.
 *
 * @author <a href="mailto:hi@alexmic.net"> Alex Michael </a>
 */

/**
 * @namespace The global namespace object. Everything is under this namespace to 
 * avoid collisions with other libraries and to have all the code under one object.
 */

var IT = IT || {};

/**
 * The XSRF token.
 */
IT.xsrf = null;

/**
 * Callback to be called when the page has finished loading.
 */
IT.onPageLoadCallback = null;

/**
 * Registers a callback to be called when the page
 * has finished loading. Calling this function or setting
 * IT.onPageLoadCallback directly will have the same effect.
 */
IT.onPageLoad = function(fn)
{
    IT.onPageLoadCallback = fn;
};

/**
 * Executes the registered callback (if any) for the current page. 
 * This is called after all the JS scripts have been loaded and
 * any necessary initialization code has been executed.
 */
IT.pageLoad = function()
{
    var fn = IT.onPageLoadCallback;
    if (fn) { fn(); }
};

/**
 * A Blurb notifier for errors.
 */
IT.errorNotifier = new Blurb({
    cssClass: "error-notify",
    position: "center-center",
    displayDuration: -1,
    content: "An error occured."
});

/**
 * A general Blurb notifier.
 */
IT.notifier = new Blurb({
    cssClass: "notify",
    position: "center-center",
    displayDuration: 1400
});

/**
 * A success Blurb notifier.
 */
IT.successNotifier = new Blurb({
    cssClass: "success-notify",
    position: "center-center",
    displayDuration: 1400,
    showCloseButton: false
});

/**
 * A popup Blurb notifier.
 */
IT.popup = new Blurb({
     cssClass: "notify",
     position: "center-center",          
     displayDuration: -1,
     wrap: true
});

/**
 * A popup Blurb notifier for other countries.
 */
IT.popupCountries = new Blurb({
     cssClass: "other-countries-blurb",	
     position: "center-center",          
     displayDuration: -1,
     wrap: true
});

    
/**
 * Shortcut AJAX POST method. Only the url parameter is required for the method to
 * work, all the others are optional.
 *  
 * @param {String} url The POST url.
 * @param {JSON} data The data to send to the server.
 * @param {Boolean} showLoader A flag indicating whether to show the loader or not.
 * @param {Function} success A function to be called if the request succeeds.
 * @param {Boolean} showErrNotifier A flag indicating whether to show an error popup or not.
 * @param {Function} error A function to be called if the request results to an error.
 */
IT.post = function(url, data, showLoader, success, showErrNotifier, error)
{
    if (!url) {
        throw "No URL defined in IT.post().";
    }
    if (showErrNotifier === null || showErrNotifier === undefined) {
        showErrNotifier = true;
    }
    IT.ajax(url, 
             data || {}, 
             success || function(){;}, 
             error || function(){;}, 
             "POST",
             showLoader || false,
             showErrNotifier);
};

/**
 * Shortcut AJAX GET method. Only the url parameter is required for the method to
 * work, all the others are optional.
 *  
 * @param {String} url The GET url.
 * @param {JSON} data The data to send to the server.
 * @param {Boolean} showLoader A flag indicating whether to show the loader or not.
 * @param {Function} success A function to be called if the request succeeds.
 * @param {Boolean} showErrNotifier A flag indicating whether to show an error popup or not.
 * @param {Function} error A function to be called if the request results to an error.
 */
IT.get = function(url, data, showLoader, success, showErrNotifier, error)
{
    if (!url) {
        throw "No URL defined in IT.get().";
    }
    if (showErrNotifier === null || showErrNotifier === undefined) {
        showErrNotifier = true;
    }
    IT.ajax(url, 
            data || {}, 
            success || function(){;}, 
            error || function(){;}, 
            "GET",
            showLoader || false,
            showErrNotifier);
};

/**
 * The core AJAX method. It acts as a wrapper to the jQuery.ajax() method,
 * adding support for a loader and some automatic error handling.
 *  
 * @param {String} url The url.
 * @param {JSON} data The data to send to the server.
 * @param {Function} success A function to be called if the request succeeds.
 * @param {Function} error A function to be called if the request results to an error.
 * @param {String} method The HTTP method.
 * @param {Boolean} showLoader A flag indicating whether to show the loader or not.
 * @param {Boolean} showErrNotifier A flag indicating whether to show an error popup or not.
 */
IT.ajax = function(url, data, success, error, method, showLoader, showErrNotifier)
{
    var requestCompleted = false;
    var loader = null;
    if (showLoader) {
        loader = $("#loader");
        if (loader.length > 0 && !loader.is(":visible")) {
            window.setTimeout(function(){
                if (!requestCompleted) {
                    loader.show();
                }
            }, 200);
        }
    }
    data["_xsrf"] = IT.xsrf;
    $.ajax({
        url: url,
        data: data,
        type: method,
        success: function(response) {
            requestCompleted = true;
            if (loader) {
                loader.hide();
            }
            if (response.s) {
                success(response);
            } else {
                if (showErrNotifier) { 
                    IT.errorNotifier.show(response.err);
                }
                error(response);
            }
        },
        statusCode: {
            500: function() {
                requestCompleted = true;
                loader.hide();
                IT.errorNotifier.show("<b>An unexpected error occured.</b><br><br> " +
                		"We are working on fixing that now. Please try again.");
                error();
            },
            403: function() {
                requestCompleted = true;
                loader.hide();
                IT.errorNotifier.show("<b>Unauthorized.</b><br><br>" + IT.fn.translateText("You are not authorized to perform this operation. Please login.", IT.user.locale))
            }
        }
    });
};

/**
 * Adds a custom module under the IT namespace.
 * 
 * Usage:
 * <pre>
 * function MyModule() {;}
 * 
 * IT.addModule("myModule", MyModule);
 * </pre>
 * 
 * @param {String} name The (unique) name of the module.
 * @param {Function} module A reference to the module to add.
 */
IT.addModule = function(name, module)
{
    if (!IT[name]) {
        IT[name] = new module();
    } else {
        throw "Module " + name + " already exists under the IT namespace.";
    }
}


//============================ IT User Module ================================ //


/**
 * Global user module. Used to store properties about the
 * current user and provides utility functions.
 */
IT.user = {
    
    // Properties.
    authenticated: false,
    uid: null,
    fbid: null,
    votes: 0,
    locale: null,	
    
    // Utility functions.
    restrictAccess: function(selector, e, callback, live) 
    {
        var fn = (live) ? "live" : "bind";
        var that = this;
        $(selector)[fn](e, function(e) {
            if (!that.authenticated) {
                var $this = $(this);
                var tag = $this[0].tagName.toLowerCase(); 
                if (tag === "input" || tag === "textarea") {
                    var tmpl = $($("#restricted-template").tmpl());
                    var pos = $this.position();
                    tmpl.insertBefore($this);
                    var padding = $this.css("padding-top") + " " +
                                  $this.css("padding-right") + " " +
                                  $this.css("padding-bottom") + " " +
                                  $this.css("padding-left");
                    tmpl.css({"top": pos.top, 
                              "left": pos.left,
                              "height": $this.height(),
                              "width": $this.width(),
                              "padding": padding,
                              "line-height": $this.height() + "px"});
                    $this.attr("readonly", "readonly");
                    window.setTimeout(function() { tmpl.fadeOut(); }, 5000);
                }
            } else {
                callback.apply(this, [e]);
            }
        });
    }
};


//============================ IT Global Function ================================ //


/**
 * Global functions module.
 */
IT.fn = {
        
    /**
     * Checks if the HTML fragment contains content by stripping away all HTML tags.
     * 
     * @param {String} fragment The HTML fragment.
     * @return {Boolean} Contains content or not.
     */
    hasContent: function(fragment)
    {
        if (!fragment) { return false; }
        var strippedText = fragment
                            .replace(/<\/?[^>]+(>|$)/g, "")
                            .replace(/&nbsp;/g, "")
                            .replace(/\s/g, "");
        return strippedText !== "" && strippedText !== " ";
    },
    
    /**
     * Like hasContent() but for varargs.
     */
    haveContent: function()
    {
        for (arg in arguments) {
            if (arguments.hasOwnProperty(arg)) {
                if (!this.hasContent(arguments[arg])) {
                    return false;
                }
            }
        }
        return true;
    },
    
    /**
     * Truncates a text blob based on maxHeight and appends an ellipsis
     * and a 'view more' button. 
     * 
     * @param {Array} elems An array of element identifiers (classes, ids) to apply
     *                      truncation on.
     * @param {Number} maxHeight The maximum height of the element, after which it will
     *                           get truncated.
     */
    truncateTextBlobs: function(elems, maxHeight, root)
    {
        for (e in elems) {
            if (elems.hasOwnProperty(e)) {
                var elemsIdentifier = elems[e];
                if (root) {
                    var $elems = root.find(elemsIdentifier);
                } else {
                    var $elems = $(elemsIdentifier);
                }
                var i; for (i=0; i < $elems.length; i++) {
                    var $elem = $($elems[i]);
                    if ($elem.height() > maxHeight) {
                        var original = $elem.html(); 
                        var truncated = original.substring(0, 200) 
                                        + "... <a class='view-more'>(view more)</a>";
                        $("<div class='original-html'>" + original + "</div>").insertAfter($elem);
                        $elem.html(truncated);
                    }
                }
            }
        }
    },
    
    /**
     * Reloads a page - extra checks for URL fragment.
     */
    reloadPage: function() 
    {
        location.href = location.href.split("#")[0];
    },
    
    /**
     * Checks the url of the current page - if it finds a fragment it looks
     * for an item having that fragment as id and highlights it.
     */
    highlightURLFragment: function()
    {
        if (location.href.indexOf("#") > -1 && location.href.indexOf("#!") === -1) {
            var locTokens = location.href.split("#");
            if (locTokens.length == 2) {
                var id = "#" + locTokens[1];
                var elem = $(id);
                if (elem.length > 0) {
                    elem.effect("highlight", {}, 2500);
                } else {
                    if (locTokens[0].indexOf("/p/") > -1) {
                        //IT.errorNotifier.show("<b>We can't find this answer.</b><br><br> " +
                        //"It's possible that the author has deleted it.");  
                    }
                }
            }
        }
    },
    
    unescape: function(word)
    {
        if (word) {
            //return word;
            var escaped = unescape(word);
            return escaped.replace(/\+/g, " ");
        }
    },

    /**
     * Translates text to Greek. It loads the dictionary from
     * translation.js.	
    */
    translateText: function(text, locale)
    {
	//If user locale is Greek or a non user translate
	if (locale == "el_GR" || locale == null){ 
		$.i18n.setDictionary(dictionary);
		return $.i18n._(text);
	}
	return text;	
    }
};

//============================ Notiffic ================================ //

/**
 * @class
 * The notification "manager" class. Does everything from showing the notification
 * box, to loading new notifications and marking them as read.
 */
var Notiffic = function(nid)
{
    var target = $(nid);
    var container = $("#notifications");
    var xhrTarget = container.find("#xhr-target");
    
    /**
     * Hooks up the notifications container to the notifications
     * 'target' i.e the notifications count button.
     */
    this.hook = function() 
    {
      var that = this;
      target.click(function(e) { 
          var left = target.offset().left + target.width() - container.width();
          container.css("left", left);
          if ($(this).hasClass("dd-up")) {
              that.open();
          } else {
              that.close();
          }
          e.stopPropagation();
      });
      
      $("#n-clear-btn").click(function(e) {
          that.clearNotifications();
          e.stopPropagation();
      });
      
      $("#n-show-all").click(function(e) {
          that.close();
          e.stopPropagation();
          location.href = $(this).attr("href");
      });
      
      $(".n-click").live("click", function() {
          location.href = $(this).attr("click-url");
      });
      
      // Make sure to close this on click anywhere else.
      $(document).click(function() {
          IT.notiffic.close();
      });
    
    };
    
    this.loadUserNotifications = function()
    {
        var that = this;
        xhrTarget.addClass("loading");
        IT.post("/u/notifications", {min: 5}, false, function(response) {
            if (response.s) {
                xhrTarget.html(response.html).removeClass("loading");
                var unread = xhrTarget.find(".unread").length;
                if (unread > 0 ) {
                    target.addClass("has-n").find("span").show().html(unread)
                }
            }
        });
    };
    
    this.clearNotifications = function()
    {
        IT.post("/u/notifications/clear", {}, true, function(response) {
           if (response.s) {
               container.find(".unread").removeClass("unread");
               target.find("span").hide();
               target.removeClass("has-n");
               $("#n-clear-btn").html(IT.fn.translateText("Clear unread"), IT.user.locale);
           } 
        });
    };
    
    this.close = function()
    {
        target.removeClass("dd-down").addClass("dd-up");
        container.hide();
    };
    
    this.open = function()
    {
         container.show();
         container.find("a, div").css("display", "block");
         target.removeClass("dd-up").addClass("dd-down");
         this.loadUserNotifications();
    };
};

IT.notiffic = new Notiffic("#n-btn");
IT.notiffic.hook();


//============================ Navigator ================================ //


/**
 * @class
 * Inspects the location.href property to properly render the page in
 * order to overcome the 'back button' ajax problem. Stores callback
 * functions to execute for a given page.
 */
var Navigator = function() 
{
    /**
     * @public
     * The last page that was recorded.
     */
    this.lastPage = null;
    
    /**
     * @public 
     * The last page's params.
     */
    this.lastPageParams = {};
    
    /**
     * @private 
     * A map of <page, function> pairs. The function is called
     * when page is loaded.
     */
    var pageActions = {};
    
    /**
     * @private
     * A map of callbacks to be called on various events.
     */
    var callbacks = {};
    
    /**
     * The period of inspecting the page.
     */
    this.inspectFrequency = 50;
    
    /**
     * Registers a callback to be called before the page function.
     * 
     * @param {Function} callback The function to be called.
     */
    this.prePageAction = function(callback) 
    {
        callbacks["prePageAction"] = callback;
    };
    
    /**
     * Checks if a new page is requested and calls the appropriate
     * action. Sets a new timeout at the end.
     */
    this.inspectPage = function()
    {
        var locationHref = window.location.href + "";
        var hrefTokens = locationHref.split("#!");
        if (hrefTokens.length > 2 || hrefTokens.length < 1) {
            throw "Wrong URL format: " + location.href;
        }
        if (hrefTokens.length == 2) {
            var page = hrefTokens[1].substring(1);
            if (page !== this.lastPage) {
                this.lastPage = page;
                this.executePageCallback(page);
            }
        } else {
            // If we've seen a last page it means we've loaded an ajax page
            // through Navigator. Now, we don't see any #! tokens, hence
            // we have pressed the back button. Pressing a link would cause the
            // page to reload hence no lastPage would exist. We thuns need to just 
            // reload the page that the addess bar is showing.
            if (this.lastPage) {
                location.href = hrefTokens[0];
                this.lastPage = null;
                return;
            }
        }
        window.setTimeout($.proxy(this.inspectPage, this), this.inspectFrequency);
    };
    
    /**
     * Execute the new page's callback. Call any prePageAction callbacks as well.
     */
    this.executePageCallback = function(page) 
    {
        var pageTokens = page.split("?");
        if (pageTokens.length > 2 || pageTokens.length < 1) {
            throw "Wrong URL format: " + location.href;
        }
        var params = {};
        if (pageTokens.length == 2) {
            params = this.resolveParams(escape(pageTokens[1]));
            this.lastPageParams = params;
        }
        callbacks["prePageAction"](page, params);
        pageActions[pageTokens[0]](params, page);
    };
    
    /**
     * Returns a hash of params from a querystring.
     */
    this.resolveParams = function(qs)
    {
        var params = {};
        var qsTokens = qs.split("&");
        var i; for (i=0; i < qsTokens.length; i++) {
            var p = unescape(qsTokens[i]);
            var paramTokens = p.split("=");
            if (paramTokens.length !== 2) {
                throw "Wrong URL format: " + location.href;
            }
            params[paramTokens[0]] = paramTokens[1];
        }
        return params;
    };
    
    /**
     * Registers a function to be called on a page. A page is what follows
     * after /#!/ and before ? in the address bar.
     * 
     * @param {String} page The page.
     * @param {Function} fn The function to be called.
     */
    this.addPageAction = function(page, fn)
    {
        pageActions[page] = fn;
    };
    
    /**
     * Initialization function.
     */
    this.init = function() 
    {
        this.inspectPage();
    };
    
};

IT.navigator = new Navigator();


// ============================ CYAPI ================================ //


/**
 * @class
 * A wrapper around the exposed API.
 */
var ITAPI = function() 
{
    /**
     * Gets the activity feed.
     * 
     * @param {Object} params The parameters which control the activity feed format. 
     *                        Valid parameters are 'page', 'limit', 'timeStep'.
     * @param {Function} cback The callback to call on success.
     */
    this.getActivity = function(params, cback)
    {
        IT.get("/getter/activity", params, true, cback);
    };

    /**
     * Gets the paragraphs.
     * 
     * @param {Object} params The parameters which control the activity feed format. 
     *                        Valid parameters are 'topic''.
     * @param {Function} cback The callback to call on success.
     */
    this.getParagraphs = function(params, success)
    {
        IT.get("/getter/p", params, true, success);
    };

    /**
     * Gets the topics.
     * 
     * @param {Object} params The parameters which control the activity feed format. 
     *                        Valid parameters are 'topic''.
     * @param {Function} cback The callback to call on success.
     */
    this.getTopics = function(params, success)
    {
        IT.get("/getter/topics", params, true, success);
    };

    /**
     * Gets the news wire.
     * 
     */
    this.getNewsWire = function(params, success)
    {
        IT.get("/getter/newswire", params, true, success);
    };
    
    this.getArticles = function(params, success)
    {
        IT.get("/getter/articles", params, true, success);
    };
    
    this.getNotifications = function(params, success)
    {
        IT.get("/getter/notifications", params, true, success);
    };

    /**
     * Gets the readings.
     * 
     */
    this.getReadings = function(params, success)
    {
        IT.get("/getter/readings", params, true, success);
    };

    /**
     * Gets the other countries.
     * 
     */
    this.getCountries = function(params, success)
    {
        IT.get("/getter/countries", params, true, success);
    };

    /**
     * Gets the explanation of a term.
     * 
     */
    this.getExplanation = function(params, success)
    {
        IT.get("/getter/explanation", params, true, success);
    };

    /**
     * Gets the user proposed paragraphs.
     * 
     */
    this.getProposals = function(params, success)
    {
        IT.get("/getter/proposals", params, true, success);
    };
    
    /**
     * Gets the data for timeline.
     * 
     */
    this.getTimeline = function(params, success)
    {
        IT.get("/getter/timeline", params, true, success);
    };
    
     /**
     * Gets the data for dictionary.
     * 
     */
    this.getDictionary = function(params, success)
    {
        IT.get("/getter/dictionary", params, true, success);
    };

}

IT.api = new ITAPI();

// ================================================== //

// Save a reference to the xsrf token.
IT.xsrf = $("input[name='_xsrf']").val();

// Check if a fragment exists in the URL and highlight anything
// with that fragment as id.
IT.fn.highlightURLFragment();

// Check if a 'view-story' element exists.
$("a.view-story").live("click", function() {
   var c =$(this).parent().siblings(".related");
   if (c.is(":visible")) {
       $(this).html(IT.fn.translateText("View more", IT.user.locale));
       c.hide();
   } else {
       $(this).html(IT.fn.translateText("Hide", IT.user.locale));
       c.show();
   }
});

//Open feedback popup.
$("#feedback").click(function() {
    var tmpl = $("#feedback-template").tmpl();
    if (!IT.popup.elem().is(":visible")) {
        IT.popup.show(tmpl);
    }
});

$("a.feedback-btn").live("click", function() {
    var type = $("#type").val();
    var description = $("#description").val();	
    IT.post("/admin/beta/feedback", 
	    {type: type, description:description}, 
	    true, function(response) {
		    if (response.s) {
		        IT.successNotifier.show(IT.fn.translateText("Thank you for helping us make our website better.", IT.user.locale));
		        IT.popup.close();
		        window.setTimeout(function() { IT.fn.reloadPage(); }, 900);		
		    } 
    });
});

$("a.no-feedback-btn").live("click", function() {
    IT.popup.close();
});

//Position the loader on the page.
var y = $(window).height() / 2 - 31;
var x = $(window).width() / 2 - 31; 
var loader = $("#loader");
if (loader.length > 0) {
    loader.css({
        left: x,
        top: y
    });
}

// Override console so it doesn't break in IE.
if (typeof console === "undefined") {
    window.console = {
        log: function () {}
    };
}



