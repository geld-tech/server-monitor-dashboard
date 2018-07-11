#!/usr/bin/env python
"""
    Server Dashboard
    Display server resources usage
"""
import ConfigParser
import logging
import logging.handlers
import os
import platform
import psutil
import time
import socket
from optparse import OptionParser
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug = True

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/server/hostname")
def server_hostname():
    hostname = get_server_hostname()
    if hostname:
        return jsonify({'hostname': hostname}), 200
    else:
        return jsonify({"cpu_temp": "localhost", "error": "Couldn't read hostname, check logs for more details.."}), 500


@app.route("/server/temperature")
def server_temperature():
    cpu_temp = get_server_temperature()
    if cpu_temp:
        return jsonify({'cpu_temp': cpu_temp}), 200
    else:
        return jsonify({"cpu_temp": "-273.15", "error": "Couldn't read temperature, check logs for more details.."}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


def get_server_temperature(self):
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
            cpu_temp = int(temp_file.read()) / 1000
        return cpu_temp
    except Exception, e:
        logger.error('Error reading temperature: %s' % e)
        return False


def get_server_hostname(self):
    try:
        hostname = socket.gethostname()
        return hostname
    except Exception, e:
        logger.error('Error reading hostname: %s' % e)
        return False


def get_server_platform(self):
    try:
        platform = platform.platform()
        return platform
    except Exception, e:
        logger.error('Error reading plaftorm: %s' % e)
        return False


def get_server_uptime(self):
    try:
        uptime = time.time() - psutil.BOOT_TIME
        return uptime
    except Exception, e:
        logger.error('Error reading uptime: %s' % e)
        return False


def get_server_cpu_percent(self):
    try:
        os_proc = psutil.Process(os.getpid())
        cpu_percent = os_proc.cpu_percent()
        return cpu_percent
    except Exception, e:
        logger.error('Error reading CPU percentage: %s' % e)
        return False


def get_server_memory_percent(self):
    try:
        os_proc = psutil.Process(os.getpid())
        mem_percent = os_proc.get_memory_info()[0] / float(2 ** 20)
        return mem_percent
    except Exception, e:
        logger.error('Error reading Memory percentage: %s' % e)
        return False


def get_server_processes(self):
    try:
        processes = []
        for proc in psutil.process_iter():
            if proc.pid > 1:
                process = {'pid': proc.pid, 'name': proc.name(), 'cpu_percent': proc.cpu_percent()}
                processes.append(process)
        return processes
    except Exception, e:
        logger.error('Error retrieving processes: %s' % e)
        return False


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
