# -*- coding: utf-8 -*- 

import web
import sys
from web.contrib.template import render_jinja
import random

# Change default Python encoding to UTF-8
reload(sys) 
sys.setdefaultencoding('utf-8')

# Init our application, this is just about the most basic setup
app = webapp2.WSGIApplication([('/', MainPage)],debug=True)
render = render_jinja('/var/www/Website-SST/website/templates', encoding = 'utf-8')
urls = ('/', 'Index')
app = web.application(urls, globals())

class Index:
    def GET(self):
        # Generate 10 random numbers
        random_numbers = [random.randrange(0, 100) for i in xrange(10)]

        # Try to pass a "bad" variable, which could be a
        # result of an attack on your website
        bad_var = '<script>alert("gotcha");</script>';

        return render.jinja(name='John Doe', number=random.randrange(0, 100),
                            numbers=random_numbers, script=bad_var)

application = app.wsgifunc()

if __name__=="__main__":
    app.run()

