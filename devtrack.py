#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import cgi
import datetime
import webapp2
import jinja2
import json

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape']
)

environment_key = ndb.Key('DevEnvironments', 'dev_environments')

class DevBox(ndb.Model):
  developer = ndb.StringProperty()
  ip_address = ndb.StringProperty()
  domain_name = ndb.StringProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    variables = {}
    variables.boxes = ndb.gql('SELECT * '
                        'FROM DevEnvironments '
                        'WHERE ANCESTOR IS :1 '
                        'ORDER BY date DESC LIMIT 10',
                        environment_key)
    self.response.out.write(template.render(variables))

class Register(webapp2.RequestHandler):
  def get(self):
    dbox = ndb.gql(('SELECT * '
            'FROM DevEnvironments '
            'WHERE developer = {}'
           ).format(self.request.get('developer'),environment_key))
    if(len(dbox)>0):
        d = iter(dbox)
        devbox = d.next()
    else:
        devbox = DevBox(parent=environment_key)

    devbox.content = self.request.get('content')
    devbox.developer = self.request.get('developer')
    devbox.ip_address = self.request.get('ip_address')
    devbox.domain_name = self.request.get('domain_name')
    devbox.put()
    
    
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/register', Register)
], debug=True)
