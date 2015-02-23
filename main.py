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
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import webapp2
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

RESTAURANT_LIST = 'restaurantList'
FEEDBACK_LIST = 'feedbackList'

def restaurantList_key(restaurantList_name=RESTAURANT_LIST):
	return ndb.Key('RestaurantList', restaurantList_name)

def feedbackList_key(feedbackList_name=FEEDBACK_LIST):
	return ndb.Key('FeedbackList', feedbackList_name)

class Restaurant(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	nationality = ndb.StringProperty(indexed=True)
	cost = ndb.StringProperty(indexed=False)
	random_description = ndb.StringProperty(indexed=False)

class Feedback(ndb.Model):
	name = ndb.StringProperty(indexed=False)
	comments = ndb.TextProperty(indexed=False)

class MainHandler(webapp2.RequestHandler):
    def get(self):

    	nationalities_query = Restaurant.query(projection=["nationality"], distinct=True)
    	nationalities = nationalities_query.fetch()
    	
    	restaurants_query = Restaurant.query(
    				ancestor=restaurantList_key(RESTAURANT_LIST)).order((Restaurant.name))

    	restaurants = restaurants_query.fetch()

    	filters = []

    	for i in range(0, len(nationalities)):
    		if(self.request.get(nationalities[i].nationality) == 'on'):
    			filters.append((restaurants_query.filter(Restaurant.nationality == nationalities[i].nationality)).fetch())

    	for i in range(0, len(filters)):
    		if(i == 0):
    			restaurants = filters[0]
    		else:
    			restaurants += filters[i]
    
    	template_values = {
    		'restaurants': restaurants,
    		'nationalities': nationalities,
    	}

    	template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    	self.response.write(template.render(template_values))

class AboutHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/about.html')
		self.response.write(template.render())

class FeedbackHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/feedback.html')
		self.response.write(template.render())

class AdminHandler(webapp2.RequestHandler):
	def get(self):
		#checks for active Google account session
		user = users.get_current_user()

		#check to see if the user is admin
		if users.is_current_user_admin():
			template_values = {
			'username': user.nickname(),
			'logout': users.create_logout_url('/admin'),
			}
			template = JINJA_ENVIRONMENT.get_template('templates/admin.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

class PostRestaurant(webapp2.RequestHandler):
	def post(self):
		#only admin can post restaurants
		user = users.get_current_user()
		if users.is_current_user_admin():
			restaurantList_name = self.request.get('restaurantList_name', RESTAURANT_LIST)

			restaurant = Restaurant(parent=restaurantList_key(restaurantList_name))

			restaurant.name = self.request.get('name')
			restaurant.nationality = self.request.get('nationality')
			restaurant.cost = self.request.get('cost')
			restaurant.random_description = self.request.get('random_description')

			restaurant.put()

			self.redirect('/admin')
		else:
			self.redirect(users.create_login_url(self.request.uri))

class PostFeedback(webapp2.RequestHandler):
	def post(self):
		feedbackList_name = self.request.get('feedbackList_name', FEEDBACK_LIST)
		feedback = Feedback(parent=feedbackList_key(feedbackList_name))

		feedback.name = self.request.get('name')
		feedback.comments = self.request.get('feedback')

		feedback.put()
		
		self.redirect('/feedback')

	
#sends an email filled with feedback
class MailBag(webapp2.RequestHandler):
	def get(self):
		feedback_query = Feedback.query()
		feedback = feedback_query.fetch()

		#if there is no feedback currently, don't send an email.
		if(feedback != []):
			#create message
			body = "mmmorblegh feedback from the past two days: (" + str(len(feedback)) + " messages)\n\n"
			for message in feedback:
				body += "User: " + message.name + "\n"
				body += "Feedback: " + message.comments + "\n\n"

			mail.send_mail(sender="mmmorblegh <cargillj@onid.oregonstate.edu>",
            	to="John Cargill <john.cargill@hotmail.com>",
            	subject="mmmorblegh mailbag",
            	body=body)

			#remove feedback from datastore
			for message in feedback:
				message.key.delete()

		else:
			pass

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/feedback', FeedbackHandler),
    ('/admin', AdminHandler),
    ('/add_restaurant', PostRestaurant),
    ('/add_feedback', PostFeedback),
    ('/mail_feedback', MailBag),
], debug=True)
