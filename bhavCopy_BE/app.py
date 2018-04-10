import requests
import redis
import os
import json
import csv
import cherrypy
import collections
import cherrypy.process.plugins
import pickle
import operator
from cherrypy.lib import static
from datetime import time, timedelta, datetime
from urllib2 import urlopen
from zipfile import ZipFile
import requests
from io import BytesIO
import redis
import tempfile
from contextlib import closing

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

conn = redis.Redis('localhost')

def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	pass


class BhavCopyView(object):
	@cherrypy.expose
	def index(self):
		bhav_copy = conn.hgetall("BhavCopy")
		load_data = (pickle.loads(bhav_copy['data']))
		newlist = sorted(load_data, key=lambda x: float(x['close']), reverse=True)
		topTen = newlist[:10]
		cherrypy.response.status = 200
		return json.dumps({"topTen" : topTen, 'status':200})

	@cherrypy.expose
	def insertData(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'

		yesterday = datetime.today() - timedelta(1)
		year, month, day = yesterday.strftime("%y"), yesterday.strftime("%m"), yesterday.strftime("%d")
		try:
			with closing(urlopen('http://www.bseindia.com/download/BhavCopy/Equity/EQ'+day+''+month+''+year+'_CSV.ZIP')) as zipresp:
				with ZipFile(BytesIO(zipresp.read())) as zfile:
					zfile.extractall('tmp/mystuff4')
					zfile.close()
		except (Exception) as e:
			pass

		try:
			with open(os.path.join("tmp/mystuff4/EQ"+day+''+month+''+year+".CSV")) as f_obj:
				reader = csv.DictReader(f_obj, delimiter=',')
				bhavList = []
				for line in reader:
					items = {
						"name":line['SC_NAME'],
						"code":line['SC_CODE'],
						"open": line['OPEN'],
						"close":line['CLOSE'],
						"low": line['LOW'],
						"high": line['HIGH']
					}
					bhavList.append(items)
				bhavObject = {}
				bhavObject['data'] = pickle.dumps(bhavList)
				conn.hmset('BhavCopy', bhavObject)
				cherrypy.response.status = 200
				return json.dumps({'message':'BhavCopy Saved Successfully', 'status':200})
		except(IOError)as e:
			cherrypy.response.status = 200
			return json.dumps({'message':'May be yesterday\'s stocks rate are not Available, You are looking at old stocks.' , 'status':200})

	@cherrypy.expose
	def search(self, query):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		bhav_copy = conn.hgetall("BhavCopy")
		load_data = (pickle.loads(bhav_copy['data']))
		search_result = []
		for i in load_data:
			if query.lower() in i['name'].lower():
				search_result.append(i)
			else:
				pass
		cherrypy.response.status = 200
		return json.dumps({'message':search_result, 'status':200})





if __name__ == '__main__':
        conf = {
                '':{
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.CORS.on': True,
                'tools.response_headers.headers': [("Access-Control-Allow-Origin", "*")],
                }
        }
        cherrypy.config.update({'tools.CORS.on': True})
        cherrypy.config.update({'server.socket_host': '0.0.0.0',})
        cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000'))})
        cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
        cherrypy.quickstart(BhavCopyView(), '/', conf)
