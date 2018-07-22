#!/usr/bin/env python
"""
    Server Dashboard
    Display server resources usage
"""
import ConfigParser
import logging
import logging.handlers
from optparse import OptionParser
from flask import Flask, render_template, jsonify

from modules.ServerMetrics import ServerMetrics
from modules.Models import Base, Server, SystemInformation, SystemStatus, Process

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

server_metrics = ServerMetrics()

# DB Session
db_path = '/dev/shm/monitor-collectord.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/server", strict_slashes=False)
@app.route("/server/usage", strict_slashes=False)
def server_usage():
    try:
        data = server_metrics.poll_metrics()
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server resources usage: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources usage, check logs for more details..'}), 500


@app.route("/server/status", strict_slashes=False)
def server_status():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for sys_status in db_session.query(SystemStatus).filter_by(server=server):
            status = {}
            status['cpu_percent'] = sys_status.cpu_percent
            status['vmem_percent'] = sys_status.vmem_percent
            status['cpu_temp'] = sys_status.cpu_temp
            status['date_time'] = sys_status.date_time
            data.append({server_metrics.get_server_hostname(): status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server resources usage: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.route("/server/information", strict_slashes=False)
def server_information():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for sys_info in db_session.query(SystemInformation).filter_by(server=server):
            status = {}
            status['platform'] = sys_info.platform
            status['system'] = sys_info.system
            status['release'] = sys_info.release
            data.append({server_metrics.get_server_hostname(): status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server information: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.route("/processes/history", strict_slashes=False)
def processes_history():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for proc_status in db_session.query(Process).filter_by(server=server):
            status = {}
            status['pid'] = proc_status.pid
            status['name'] = proc_status.name
            status['cpu_percent'] = proc_status.cpu_percent
            status['date_time'] = proc_status.date_time
            data.append({proc_status.name: status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving processes history: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.route("/server/hostname")
def server_hostname():
    hostname = server_metrics.get_server_hostname()
    if hostname:
        return jsonify({'hostname': hostname}), 200
    else:
        return jsonify({"cpu_temp": "localhost", "error": "Couldn't read hostname, check logs for more details.."}), 500


@app.route("/server/temperature")
def server_temperature():
    cpu_temp = server_metrics.get_server_temperature()
    if cpu_temp:
        return jsonify({'cpu_temp': cpu_temp}), 200
    else:
        return jsonify({"cpu_temp": "-273.15", "error": "Couldn't read temperature, check logs for more details.."}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


if __name__ == "__main__":
    # Parse options
    parser = OptionParser()
    parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0')
