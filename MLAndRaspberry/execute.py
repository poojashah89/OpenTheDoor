import time
import os

import subprocess
import sys,errno
import shutil
import datetime
from collections import Counter

# Flask is a REST Api framework in python
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
#from time import sleep

# initialize Flask
app = Flask(__name__)
api = Api(app)

class recognize(Resource):
	def get(self):
		foundName = []
		st = subprocess.check_output("face_recognition --tolerance 0.43 ./known/ ./unknown/",shell=True)
		fo = open("output.txt", "rw+")
		line = fo.writelines(st)
		fo.close()

		try:
			source = open('output.txt','r')
        		for line in source:
        			line = line.split(",")
                		foundName.append(line[1])
                		#sys.stdout.write(line)
        		source.close()
		except IOError as e:
       			if e.errno == errno.EPIPE:
          			print(e.errno)

		#print(foundName)
		countName = Counter(foundName).most_common(1)[0]
		print(countName[0])
		#text = countName[0].split(",",1)[1]
		text = countName[0].split("\n",1)[0]
		print(text)
		st = datetime.datetime.now().strftime("%d-%m-%y-%X")
		srcfile = '/home/ubuntu/unknown/image0.jpg'
		dstroot = '/home/ubuntu/history/' + text + st + '.jpg'
		shutil.copy(srcfile, dstroot)
 		return { 'Name' : text }


# Get the list of contacts from the folder
class List(Resource):
    def get(self):
    	tree = dict(name=os.path.basename("known/"), children=[])
    	try: lst = os.listdir("known/")
    	except OSError:
        	pass #ignore errors
    	else:
        	for name in lst:
            		fn = os.path.join("known/",name)
            		tree['children'].append(dict(name=name))
    	return tree


# Get the image from contacts , filename is the image name
@app.route('/images/<path:filename>')
def serve_static(filename):
    return send_from_directory("known/", filename)


# POST to upload the image to contacts folder
@app.route('/upload/<path:filename>', methods=['POST'])
def upload_file(filename):

    # print request.files
    # checking if the file is present or not.
    if 'file' not in request.files:
        return "No file found"

    file = request.files['file']
    file.save("known/"+filename)
    return "file successfully saved"

@app.route('/history/<path:filename>')
def historyimages(filename):
        return send_from_directory("history/", filename)

class ListHistory(Resource):
    def get(self):
    	tree = dict(name=os.path.basename("/home/ubuntu"), children=[])
    	try: lst = os.listdir("history/")
    	except OSError:
        	pass #ignore errors
    	else:
        	for name in lst:
            		fn = os.path.join("history/",name)
            		tree['children'].append(dict(name=name))
    	return tree

api.add_resource(List, '/list')
api.add_resource(recognize, '/recognize')
api.add_resource(ListHistory, '/historylist')

if __name__ == '__main__':
        app.run(debug=True,host= '0.0.0.0')
