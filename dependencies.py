############################
# CSS and JS dependenciesB  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
             ("/learn/question", ["questions.css"]),			
             ("/learn/main", ["learn.css"]),			
             ("/", ["home.css"]),	
            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/admin/*", ["admin.js"]),    
             ("/", ["home.js", "libs/jquery.tmpl.min.js"]),
	    ])

