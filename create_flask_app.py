import os
import argparse

def create_flask_app(app='flask_app', threading=False, WSGIServer=False, unwanted_warnings=False, logging=False, further_logging=False, endpoints=None):
	
	lines = ["from flask import Flask, send_from_directory","import codecs"]
	print(app)
	params = {
		'app': app,
		'threading': threading,
		'WSGIServer': WSGIServer,
		'unwanted_warnings': unwanted_warnings,
		'logging': logging, 
		'further_logging': further_logging,
		'endpoints': endpoints,
	}

	if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		for param in params.keys():
			if param == 'endpoints':
				parser.add_argument('-'+param[0].lower(), '--'+param.lower(), nargs='+', help='', required=False)
			else:
				parser.add_argument('-'+param[0].lower(), '--'+param.lower(), help='', required=False)

		args = vars(parser.parse_args())
		for param in args.keys():
			if param == 'app':
				if args[param] != None:
					params[param] = args[param]
			else:
					params[param] = args[param]

	project = params['app']
	print(project)
	endpoints = params['endpoints']

	index = "<!DOCTYPE html>\n<html>\n<head>\n\t<title>endpoint</title>\n\t<link href='static/style.css' rel='stylesheet'>\n</head>\n<body>\n\n<script src='static/script.js'></script>\n</body>\n</html>".replace('endpoint', project)
	
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
		'WSGIServer': ["", "#WSGIServer", "from gevent.pywsgi import WSGIServer"],
		'unwanted_warnings': ["", "#Disable Warnings", "import warnings", "warnings.filterwarnings('ignore')"],
		'logging': ["", "#Logging", "import logging", "", "#Logging configuration set to debug on debug.log file", "logging.basicConfig(filename='debug.log',level=logging.DEBUG)", "logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')"],
		'further_logging': ["", "#Disable unneeded dependencies logging", "werkzeugLog = logging.getLogger('werkzeug')", "werkzeugLog.disabled = True", "requestsLog = logging.getLogger('urllib3.connectionpool')", "requestsLog.disabled = True"],
	}

	for param in headers.keys():
		if params[param]:
			for line in headers[param]:
				lines.append(line)

	lines.append("\ndef run():")

	if params['WSGIServer']:
		lines.append("\t#WSGIServer") 
		lines.append("\tWSGIServer(('', 8081), app).serve_forever()")
	else:
		lines.append("\tapp.run(host='0.0.0.0',port=8081)")

	if params['threading']:
		for line in ["", "#Thread", "def keep_alive():", "\tt = Thread(target=run)", "\tt.start()"]:
			lines.append(line)

	for line in ["", "app = Flask(__name__)", "", "@app.route('/')", "def main():", "\t#index.html", "\treturn codecs.open('web/index.html', 'r', 'utf-8').read()", "", "@app.route('/favicon.ico')", "def favicon():", "\treturn send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')"]:
		lines.append(line)

	if endpoints is not None:
		for ep in endpoints:
			tp = ["@app.route('/endpoint')", "def endpoint():", "\t#endpoint.html", "\treturn codecs.open('web/endpoint.html', 'r', 'utf-8').read()"]
			for line in tp:
				lines.append(line.replace('endpoint', ep))

			epFile = open(project+"/web/endpoint.html".replace('endpoint', ep),"w+")
			epFile.write(index.replace('endpoint', ep).replace('style.css', ep+'.css').replace('script.js', ep+'.js'))
			epFile.close()
			os.system('touch '+project+'/static/'+ep+'.css')
			os.system('touch '+project+'/static/'+ep+'.js')

	lines.append("if __name__ == '__main__':")
	if params['WSGIServer']:
		lines.append("\t#Threading")
		lines.append("\tkeep_alive()")
	else:
		lines.append("\t#No Threading")
		lines.append("\trun()")

	for line in lines:
		f.write(line+'\n')
	f.close()
	print('Created App ' + project)
	for param in params.keys():
		if params[param] and param != 'app':
			print(param, params[param])
	os.system('open '+ project)

if __name__ == '__main__':
	create_flask_app()