from flask import request, render_template
from flask.ext.restful import  Resource
from tracker.extensions import api


class AngularView(Resource):

	def get(self):
		return render_template('index.html')




api.add_resource(AngularView, '/', endpoint = 'index')
