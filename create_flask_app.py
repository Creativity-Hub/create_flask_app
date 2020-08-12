import os
import argparse

def check_for_pkg(pkg):
	try:
		exec("import " + pkg)
	except:
		os.system("pip3 install --user " + pkg)

def create_flask_app(app='flask_app', threading=False, wsgiserver=False, unwanted_warnings=False, logging=False, further_logging=False, site_endpoints=None, endpoints=None, request_endpoints=None):
	
	check_for_pkg('flask')

	lines = ["from flask import Flask, send_from_directory","import codecs", "import os"]

	params = {
		'app': app,
		'threading': threading,
		'wsgiserver': wsgiserver,
		'unwanted_warnings': unwanted_warnings,
		'logging': logging, 
		'further_logging': further_logging,
		'site_endpoints': site_endpoints,
		'endpoints': endpoints,
		'request_endpoints': request_endpoints
	}

	if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		for param in params.keys():
			if 'endpoints' in param:
				parser.add_argument('-'+param[0].lower(), '--'+param.lower(), nargs='+', help='', required=False)
			else:
				parser.add_argument('-'+param[0].lower(), '--'+param.lower(), help='', required=False)

		args = vars(parser.parse_args())
		for param in args.keys():
			if 'request' in param and len(args[param]) % 3 != 0:
				print('Request method endpoint format invalid, enter "Method" "Endpoint" "Parameter"')
			if param == 'app':
				if args[param] != None:
					params[param] = args[param]
			else:
					params[param] = args[param]

	index = "<!DOCTYPE html>\n<html>\n<head>\n\t<title>endpoint</title>\n\t<link href='static/style.css' rel='stylesheet'>\n</head>\n<body>\n\n<script src='static/script.js'></script>\n</body>\n</html>"

	project = params['app']

	if not os.path.exists(project):
		os.mkdir(project)
	if not os.path.exists(project+'/web'):
		os.mkdir(project+'/web')
	if not os.path.exists(project+'/static'):
		os.mkdir(project+'/static')
	os.system('touch '+project+'/static/style.css')
	os.system('touch '+project+'/static/script.js')

	indexFile = open(project+"/web/index.html","w+")
	indexFile.write(index.replace('endpoint', project))
	indexFile.close()

	f = open(project+'/'+project+".py","w+")

	headers = {
		'threading': ["", "#Threading", "from threading import Thread"],
		'wsgiserver': ["", "#WSGIServer", "from gevent.pywsgi import WSGIServer"],
		'unwanted_warnings': ["", "#Disable Warnings", "import warnings", "warnings.filterwarnings('ignore')"],
		'logging': ["", "#Logging", "import logging", "", "#Logging configuration set to debug on debug.log file", "logging.basicConfig(filename='debug.log',level=logging.DEBUG)", "logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')"],
		'further_logging': ["", "#Disable unneeded dependencies logging", "werkzeugLog = logging.getLogger('werkzeug')", "werkzeugLog.disabled = True", "requestsLog = logging.getLogger('urllib3.connectionpool')", "requestsLog.disabled = True"],
	}
	
	for param in headers.keys():
		if params[param]:
			for line in headers[param]:
				lines.append(line)

	lines.append("\ndef run():")

	if params['wsgiserver']:
		check_for_pkg('gevent')
		lines.append("\t#WSGIServer") 
		lines.append("\tWSGIServer(('', 8081), app).serve_forever()")
	else:
		lines.append("\tapp.run(host='0.0.0.0',port=8081)")

	if params['threading']:
		for line in ["", "#Thread", "def keep_alive():", "\tt = Thread(target=run)", "\tt.start()"]:
			lines.append(line)

	for line in ["", "app = Flask(__name__)", "", "@app.route('/')", "def main():", "\t#index.html", "\treturn codecs.open('web/index.html', 'r', 'utf-8').read()", "", "@app.route('/favicon.ico')", "def favicon():", "\treturn send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')"]:
		lines.append(line)


	site_endpoints = params['site_endpoints']
	if site_endpoints is not None:
		for ep in site_endpoints:
			print('Endpoint: ' + ep)
			tp = ["\n@app.route('/endpoint')", "def endpoint():", "\t#endpoint.html", "\treturn codecs.open('web/endpoint.html', 'r', 'utf-8').read()"]
			for line in tp:
				lines.append(line.replace('endpoint', ep))

			epFile = open(project+"/web/endpoint.html".replace('endpoint', ep),"w+")
			epFile.write(index.replace('endpoint', ep).replace('style.css', ep+'.css').replace('script.js', ep+'.js'))
			epFile.close()
			os.system('touch '+project+'/static/'+ep+'.css')
			os.system('touch '+project+'/static/'+ep+'.js')
	
	endpoints = params['endpoints']
	if endpoints is not None:
		for ep in endpoints:
			print('Endpoint: ' + ep)
			tp = ["\n@app.route('/endpoint')", "def endpoint():", "\t#endpoint.html", "\treturn endpoint_route"]
			for line in tp:
				lines.append(line.replace('endpoint', ep))

	request_endpoints = params['request_endpoints']
	print(request_endpoints)
	request_method = request_endpoints[0]
	if request_endpoints is not None:
		request_endpoints = [request_endpoints[i * 3:(i + 1) * 3] for i in range((len(request_endpoints) + 3 - 1) // 3)]
		for request_method, ep, request_param in request_endpoints:
			print('Endpoint: ' + ep, '\nMethod: ' + request_method, '\nParameter: ' + request_param)
			tp = ["\n@app.route('/"+ep+"/<"+request_param+">', methods=['"+request_method+"'])", "def "+ep+"("+request_param+"):", "\t#"+request_method+" method endpoint", "\treturn do_something("+request_param+")"]
			for line in tp:
				lines.append(line)

	lines.append("\nif __name__ == '__main__':")
	if params['wsgiserver']:
		lines.append("\t#Run server forever")
		lines.append("\tkeep_alive()")
	else:
		lines.append("\t#Run server")
		lines.append("\trun()")

	for line in lines:
		f.write(line+'\n')
	f.close()
	print('Created' + project + ' app succesfully.')
	for param in params.keys():
		if params[param] and param != 'app':
			print(param, params[param])

	os.system('open '+ project)

if __name__ == '__main__':
	create_flask_app()
