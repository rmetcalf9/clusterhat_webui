#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import parse_qs
import subprocess

#Web request
# when called with 0 params just serve the file
# when called for file /get_cur_status return json with current status
# ?mode=on&device=off - preform action


PORT_NUMBER = 80

POSITIONS=[1,2,3,4]

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	def RepresentsInt(self,s):
	    try: 
	        int(s)
	        return True
	    except ValueError:
	        return False

	def process_incomming_command_check_device(self,dev):
		if dev=="all":
			return True
		if dev[0]!="p":
			return False
		if self.RepresentsInt(dev[1:]):
			return True
		return False

	def process_incomming_command(self):
		respJSON = "{ \"status\": \"ERROR\" }"
		param_arr = parse_qs(self.path[2:])
		mode=str(next(iter(param_arr.get("mode") or []), None))
		device=str(next(iter(param_arr.get("device") or []), None))
		if mode=="on" or mode=="off":
			if self.process_incomming_command_check_device(device)==True:
				result_from_cmd = subprocess.check_output(["/sbin/clusterhat",mode,device])
				respJSON = "{ \"status\": \"OK\" }"

                self.send_response(200)
                self.send_header('Content-type','text/json')
                self.end_headers()
                respJSON = "{\"resp\":" + respJSON + "}"
                #print respJSON
                self.wfile.write(respJSON)
		return 

	def get_interface_list(self):
		retstr = subprocess.check_output(["ip","link","show"])
		return retstr

	def serve_cur_status(self):
		interface_list = self.get_interface_list()
		respJSON = ""
		fir = True
                for device in POSITIONS:
			if fir==False:
				respJSON += ","
			fir=False
                        statusStr = "ON"
                        if interface_list.find("ethpi" + str(device))==-1:
                                statusStr = "OFF"
			respJSON += "{"
			respJSON += " \"device\": \"p" + str(device) + "\","
			respJSON += " \"host\": \"p" + str(device) + "\","
			respJSON += " \"status\": \"" + statusStr + "\""
			respJSON += "}"
                self.send_response(200)
                self.send_header('Content-type','text/json')
                self.end_headers()
		respJSON = "{\"resp\":[" + respJSON + "]}"
		#print respJSON
                self.wfile.write(respJSON)
 
		return

	def serve_file(self):
		try:
			if self.path.endswith(".html"):
				f = open("html/" + self.path)
		                self.send_response(200)
		                self.send_header('Content-type',    'text/html')
                		self.end_headers()
                		self.wfile.write(f.read())
                		f.close()
                		return
			if self.path.endswith(".js"):
                                f = open("html/" + self.path)
                                self.send_response(200)
                                self.send_header('Content-type',    'text/javascript')
                                self.end_headers()
                                self.wfile.write(f.read())
                                f.close()
                                return
  
	        except IOError:
        	    self.send_error(404,'File Not Found: %s' % self.path)
		return
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		param_arr = parse_qs(self.path[2:])
		if self.path=="/get_cur_status":
			self.serve_cur_status() 
		elif len(param_arr)==0:
			self.serve_file()
		else:
			self.process_incomming_command()
#			print "TODO - Process message and Serve Response self.path=" + self.path

		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

