from flask import Flask,request,render_template
from flask_restful import Resource, Api
import requests
import os
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)


global perfdata

class PerfData():
    """docstring forPerfData."""
    def __init__(self):
        self.process = 0
        self.system = 0
        self.network = 0

    def get_process_data(self):
        return self.process

    def set_process_data(self,datas):
        self.process = datas

    def get_system_data(self):
        return self.system

    def set_system_data(self,datas):
        self.system = datas

    def set_network_data(self,datas):
        self.network = datas

    def get_network_data(self):
        return self.network


app = Flask(__name__)
api = Api(app)

@app.route('/')
def report():
    return render_template('report.html')

class ProcessServer(Resource):
    def get(self):
        return perfdata.get_process_data()
        # return {'hello': 'world','updated':'true'}

class SystemServer(Resource):
    def get(self):
        return perfdata.get_system_data()

class NetworkServer(Resource):
    def get(self):
        return perfdata.get_network_data()


api.add_resource(ProcessServer, '/api/proc')
api.add_resource(SystemServer, '/api/sys')
api.add_resource(NetworkServer, '/api/net')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def stop_server():
    response = requests.post('http://127.0.0.1:5000/shutdown')

def start_server(object):
    log.info("Started server")
    global perfdata
    perfdata = object
    app.run(debug=False)

# if __name__ == '__main__':
#     start_server()
