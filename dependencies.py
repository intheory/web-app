############################
# CSS and JS dependenciesB  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
             ("/learn/*", ["learn.css", "questions.css", "nuggets.css"]),			
             ("/", ["home.css"]),	
            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/admin/*", ["admin.js"]),    
             ("/", ["home.js", "libs/jquery.tmpl.min.js"]),
	    ])

