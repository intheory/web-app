############################
# CSS and JS dependenciesB  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
             ("/landing/*", ["landing.css"]),
             ("/test", ["questions.css", "test.css"]),
             ("/learn/*", ["learn.css", "nuggets.css"]),			
             ("/", ["home.css"]),	
            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/landing", ["landing.js"]),
             ("/test", ["test.js", "libs/jquery.tmpl.min.js"]),    
             ("/learn/*", ["learn.js"]),    
             ("/admin/*", ["admin.js"]),    
             ("/", ["home.js", "libs/jquery.tmpl.min.js"]),
	    ])

