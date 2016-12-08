import json
import os
import cherrypy
import redis
import fileinput

class Topgainers(object):
	@cherrypy.expose
	def index(self):
		self.connectionFlag = 1
		self.nsedata = {}
		self.connectToRedis()
		self.getData()
		self.createView()
		return open('index.html')

	def connectToRedis(self):
		try:
			self.rdb = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		except Exception, e:
			err = {}
			err["message"] = str(e)
			err["method"] = "connectToRedis"
			self.logError(err)

	def getData(self):
		try:
			if(self.rdb):
				keys = self.rdb.keys()
				# for k in self.rdb.scan_iter(match='top_*'):
				# 	self.nsedata[k] = self.rdb.hgetall(k)
				for i in range(1,11):
					self.nsedata["top_"+str(i)] = self.rdb.hgetall("top_"+str(i))
			else:
				if self.connectionFlag <= 5:
					self.connectToRedis()
					self.getData()
					self.connectionFlag += 1
				else:
					print "Maximum retry connection to redis exceeded!"
		except Exception, e:
			err = {}
			err["message"] = str(e)
			err["method"] = "getData"
			self.logError(err)

	def createView(self):
		html = ""
		count = 1
		# for data in self.nsedata:
		for i in range(1,11):
			html += '''<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 top-card-container">
						<div class="row top-card">
							<div class="col-xs-12 nse-symbol">%s</div>
							<div class="col-xs-6 nse-ltp">LTP</div><div class="col-xs-6 nse-ltp-val">%s</div>
							<div class="col-xs-6 nse-pc-change">%% Change</div><div class="col-xs-6 nse-pc-change-val">%s</div>
							<div class="col-xs-6 nse-traded-qty">Traded Quantity</div><div class="col-xs-6 nse-traded-qty-val">%s</div>
							<div class="col-xs-6 nse-value-lakhs">Value (in Lakhs)</div><div class="col-xs-6 nse-value-lakhs-val">%s</div>
							<div class="col-xs-6 nse-open">Open</div><div class="col-xs-6 nse-open-val">%s</div>
							<div class="col-xs-6 nse-high">High</div><div class="col-xs-6 nse-high-val">%s</div>
							<div class="col-xs-6 nse-low">Low</div><div class="col-xs-6 nse-low-val">%s</div>
							<div class="col-xs-6 nse-prev-close">Previous Close</div><div class="col-xs-6 nse-prev-close-val">%s</div>
							<div class="col-xs-6 nse-latest-ex-dt">Latest Ex Date</div><div class="col-xs-6 nse-latest-ex-dt-val">%s</div>
							<div class="ranking">%s</div>
						</div>
					</div>''' % (self.nsedata["top_"+str(i)]["symbol"],self.nsedata["top_"+str(i)]["ltp"],self.nsedata["top_"+str(i)]["netPrice"],self.nsedata["top_"+str(i)]["tradedQuantity"],self.nsedata["top_"+str(i)]["turnoverInLakhs"],self.nsedata["top_"+str(i)]["openPrice"],self.nsedata["top_"+str(i)]["highPrice"],self.nsedata["top_"+str(i)]["lowPrice"],self.nsedata["top_"+str(i)]["previousPrice"],self.nsedata["top_"+str(i)]["lastCorpAnnouncementDate"],count)
			count += 1
		lines = []
		with open('src-index.html') as infile:
		    for line in infile:
		    	line = line.replace("[{data}]", html)
		    	lines.append(line)
		with open('index.html', 'w') as outfile:
		    for line in lines:
		        outfile.write(line)


	def logError(self,error):
		try:
			f = open('topgainersError.log','a')
			f.write(json.dumps(error))
			f.write("\n")
			f.close()
		except Exception, e:
			print str(e)

if __name__=='__main__':
	path   = os.path.abspath(os.path.dirname(__file__))
	conf = {
		'/static': {
		            'tools.staticdir.on': True,
		            'tools.staticdir.dir' : os.path.join(path, 'public')
		        }
	}
	cherrypy.quickstart(Topgainers(),'/',conf)