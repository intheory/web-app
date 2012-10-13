############################
# CSS and JS dependenciesB  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
             ("/register", ["register.css"]),
             ("/login/options", ["login.css"]),
             ("/landing/*", ["landing.css"]),
             ("/practice/main", ["test.css"]),    
             ("/test", ["questions.css", "test.css"]),
             ("/learn/*", ["learn.css", "nuggets.css"]),			
             ("/", ["home.css"]),	
            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/landing", ["landing.js", "libs/jquery.tmpl.min.js"]),
             ("/test", ["test.js", "libs/jquery.tmpl.min.js", "libs/jquery.timer.js"]),    
             ("/learn/*", ["learn.js", "libs/jquery.tmpl.min.js"]),    
             ("/admin/*", ["admin.js"]),    
             ("/", ["home.js", "libs/jquery.tmpl.min.js"]),
	    ])

