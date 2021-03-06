#!/usr/bin/env python
"""
    Server Dashboard
    Display server resources usage
"""
import ConfigParser
import datetime
import logging
import logging.handlers
import sys
from optparse import OptionParser
from flask import Flask, render_template, jsonify

from modules.ServerMetrics import ServerMetrics
from modules.Models import Base, Server, SystemInformation, SystemStatus, Process

from sqlalchemy import cast, Date, func
from flask_sqlalchemy import SQLAlchemy

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

# Flask Application
app = Flask(__name__)
app.debug = False

# DB Session
db_path = '/dev/shm/monitor-collectord.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

server_metrics = ServerMetrics()


@app.before_first_request
def setup():
    Base.metadata.bind = db.engine


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/server", strict_slashes=False)
@app.route("/server/usage", strict_slashes=False)
def server_usage():
    try:
        now = datetime.datetime.utcnow()
        last_2_hours = now - datetime.timedelta(hours=2)
        last_5_mins = now - datetime.timedelta(minutes=5)
        data = {}

        # Identify current server
        hostname = server_metrics.get_server_hostname()
        server = db.session.query(Server).filter_by(hostname=hostname).first()

        # Retrieve current system information
        data['hostname'] = hostname
        data['platform'] = server_metrics.get_server_platform()
        data['system'] = server_metrics.get_server_system()
        data['release'] = server_metrics.get_server_release()
        data['architecture'] = server_metrics.get_server_architecture()
        data['uptime'] = server_metrics.get_server_uptime()
        data['disks_usage'] = server_metrics.get_disks_usage()
        data['swap_usage'] = server_metrics.get_swapdisk_usage()

        # Query metrics for latest resources usage
        current_stat = (
            db.session.query(SystemStatus)
            .filter(cast(SystemStatus.date_time, Date) == cast(now.date(), Date))
            .order_by(SystemStatus.id.desc())
            .first()
        )
        if current_stat:
            data['cpu_percent'] = current_stat.cpu_percent
            data['vmem_percent'] = current_stat.vmem_percent
            data['cpu_temp'] = current_stat.cpu_temp

        # Query metrics for processes data to add to table
        processes_result = (
            db.session.query(Process.pid, Process.name, func.avg(Process.cpu_percent).label('cpu_percent'), Process.date_time)
            .filter_by(server=server)
            .filter(SystemStatus.timestamp >= last_5_mins.strftime('%s'))
            .group_by(Process.pid)
            .order_by(Process.pid)
            .limit(12)
        )
        processes_data = []
        for proc_status in processes_result:
            status = {}
            status['pid'] = proc_status.pid
            status['name'] = proc_status.name
            status['cpu_percent'] = round(proc_status.cpu_percent, 1)
            status['date_time'] = proc_status.date_time
            processes_data.append(status)
        data['processes'] = processes_data

        # Query metrics for system status to plot in graphs
        system_status_result = (
            db.session.query(SystemStatus)
            .filter_by(server=server)
            .filter(SystemStatus.timestamp >= last_2_hours.strftime('%s'))
            .order_by(SystemStatus.date_time)
        )
        date_time_data, cpu_percent_data, vmem_percent_data, swap_percent_data, cpu_temp_data = [], [], [], [], []
        for sys_stat in system_status_result:
            date_time_data.append(sys_stat.date_time.strftime("%H:%M"))
            cpu_percent_data.append(sys_stat.cpu_percent)
            vmem_percent_data.append(sys_stat.vmem_percent)
            swap_percent_data.append(sys_stat.swap_percent)
            cpu_temp_data.append(sys_stat.cpu_temp)

        # Format response data to be ingested in client side
        data['graphs_data'] = {'cpu_percent': cpu_percent_data,
                               'vmem_percent': vmem_percent_data,
                               'swap_percent': swap_percent_data,
                               'cpu_temp': cpu_temp_data,
                               'date_time': date_time_data}
        return jsonify({'data': data}), 200
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error('Error retrieving server resources usage: %s (line=%d)' % (e, exc_tb.tb_lineno))
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources usage, check logs for more details..'}), 500


@app.route("/server/information", strict_slashes=False)
def server_information():
    try:
        data = []
        server = db.session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for sys_info in db.session.query(SystemInformation).filter_by(server=server):
            status = {}
            status['platform'] = sys_info.platform
            status['system'] = sys_info.system
            status['release'] = sys_info.release
            data.append({server_metrics.get_server_hostname(): status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server information: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


if __name__ == "__main__":
    # Parse options
    opts_parser = OptionParser()
    opts_parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = opts_parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0')
