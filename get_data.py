import json
import redis
import time
import urllib2
import datetime

class Getdata():

	def __init__(self):
		try:
			self.dataset = {}
			self.url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
			self.rdb = {}
			self.nsedata = {}
			self.start()
		except Exception, e:
			print "Couldn't Inititalize"
			err = {}
			err["message"] = str(e)
			err["method"] = "__init__"
			self.logError(err)


	def logError(self,error):
		try:
			f = open('error.log','a')
			f.write(json.dumps(error))
			f.write("\n")
			f.close()
		except Exception, e:
			print str(e)

	def start(self):
		self.connectToRedis()
		self.requestNseData()


	def connectToRedis(self):
		try:
			self.rdb = redis.StrictRedis(host='localhost', port=6379, db=0)
		except Exception, e:
			err = {}
			err["message"] = str(e)
			err["method"] = "connectToRedis"
			self.logError(err)


	def requestNseData(self):
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [("User-agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36"),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('Upgrade-Insecure-Requests', '1')]
			res = opener.open(self.url)
			response = res.read()
			data = json.loads(response)
			self.nsedata = data
			print self.nsedata
			self.saveDataToRedis()
		except Exception, e:
			err = {}
			err["message"] = str(e)
			err["method"] = "requestNseData"
			self.logError(err)


	def saveDataToRedis(self):
		try:
			d = self.nsedata
			logtime=0
			if "time" in d:
				logtime = time.mktime(datetime.datetime.strptime(d["time"], "%b %d, %Y %H:%M:%S").timetuple())
			count = 1
			for data in d["data"]:
				self.tophash = "top_" + str(count)
				self.rdb.hmset(self.tophash, data)
				self.datahash = str(logtime) + "___" + str(data["symbol"])
				self.rdb.hmset(self.datahash, data)
				count += 1
			self.timehash = datetime.date.today().strftime("%d-%B-%Y") + "-" + str(logtime)
			self.rdb.hmset(self.timehash, {"time":logtime})
			print time.time()
		except Exception, e:
			err = {}
			err["message"] = str(e)
			err["method"] = "saveDataToRedis"
			self.logError(err)


while(1):
	Getdata()
	waittime = 300 #seconds to wait
	time.sleep(waittime)