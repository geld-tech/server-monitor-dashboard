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


@app.route("/server", strict_slashes=False)
@app.route("/server/usage", strict_slashes=False)
def server_usage():
    try:
        hostname = get_server_hostname()
        server_os = get_server_platform()
        uptime = get_server_uptime()
        cpu_temp = get_server_temperature()
        cpu_percent = get_server_cpu_percent()
        mem_percent = get_server_memory_percent()
        procs = get_server_processes()
        disks_usage = get_disks_usage()
        disks_io = get_disks_io()
        swap_usage = get_swapdisk_usage()
        network_io = get_network_io()
        data = {'hostname': hostname,
                'platform': server_os,
                'uptime': uptime,
                'cpu_temp': cpu_temp,
                'cpu_percent': cpu_percent,
                'mem_percent': mem_percent,
                'processes': procs,
                'disks_usage': disks_usage,
                'disks_io': disks_io,
                'swap_usage': swap_usage,
                'network_io': network_io}
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server resources usage: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources usage, check logs for more details..'}), 500


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


def get_server_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
            cpu_temp = int(temp_file.read()) / 1000
        return cpu_temp
    except Exception, e:
        logger.error('Error reading temperature: %s' % e)
        return False


def get_server_hostname():
    try:
        hostname = socket.gethostname()
        return hostname
    except Exception, e:
        logger.error('Error reading hostname: %s' % e)
        return False


def get_server_platform():
    try:
        return platform.platform()
    except Exception, e:
        logger.error('Error reading plaftorm: %s' % e)
        return False


def get_server_system():
    try:
        return platform.system()
    except Exception, e:
        logger.error('Error reading operating system: %s' % e)
        return False


def get_server_architecture():
    try:
        return platform.machine()
    except Exception, e:
        logger.error('Error reading machine architecture: %s' % e)
        return False


def get_server_release():
    try:
        return platform.release()
    except Exception, e:
        logger.error('Error reading release: %s' % e)
        return False


def get_server_uptime():
    try:
        uptime = time.time() - psutil.BOOT_TIME
        return uptime
    except Exception, e:
        logger.error('Error reading uptime: %s' % e)
        return False


def get_server_cpu_percent():
    try:
        return psutil.cpu_percent(interval=1)
    except Exception, e:
        logger.error('Error reading CPU percentage: %s' % e)
        return False


def get_server_virtual_memory_percent():
    try:
        return psutil.virtual_memory().percent
    except Exception, e:
        logger.error('Error reading Virtual Memory percentage: %s' % e)
        return False


def get_server_disk_usage_percent(mountpoint='/'):
    try:
        return psutil.disk_usage(mountpoint).percent
    except Exception, e:
        logger.error('Error reading Disk Usage Mountpoint percentage: %s' % e)
        return False


def get_server_processors_count():
    try:
        return psutil.cpu_count()
    except Exception, e:
        logger.error('Error reading count of CPU: %s' % e)
        return False


def get_server_memory_percent():
    try:
        os_proc = psutil.Process(os.getpid())
        mem_percent = os_proc.memory_info()[0] / float(2 ** 20)
        return mem_percent
    except Exception, e:
        logger.error('Error reading Memory percentage: %s' % e)
        return False


def get_server_processes(max_count=12):
    try:
        processes = []
        for proc in psutil.process_iter():
            process = {'pid': proc.pid, 'name': proc.name(), 'cpu_percent': proc.cpu_percent()}
            processes.append(process)
        return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:max_count]
    except Exception, e:
        logger.error('Error retrieving processes: %s' % e)
        return False


def get_server_processes_with_memory(max_count=12):
    try:
        properties = ['username', 'nice', 'memory_info', 'memory_percent', 'cpu_percent', 'cpu_times', 'name', 'status']
        processes = []
        procs_status = {}
        for p in psutil.process_iter():
            try:
                p.dict = p.as_dict(properties)
                try:
                    procs_status[p.dict['status']] += 1
                except KeyError:
                    procs_status[p.dict['status']] = 1
            except psutil.NoSuchProcess:
                pass
            else:
                processes.append(p)
        processes = sorted(processes, key=lambda p: p.dict['cpu_percent'], reverse=True)[:max_count]
        return (processes, procs_status)  # return processes sorted by CPU and stats
    except Exception, e:
        logger.error('Error retrieving processes: %s' % e)
        return False


def get_disks_usage():
    try:
        values = []
        disk_partitions = psutil.disk_partitions(all=False)
        for partition in disk_partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            device = {'device': partition.device,
                      'mountpoint': partition.mountpoint,
                      'fstype': partition.fstype,
                      'opts': partition.opts,
                      'total': usage.total,
                      'used': usage.used,
                      'free': usage.free,
                      'percent': usage.percent
                      }
            values.append(device)
        values = sorted(values, key=lambda device: device['device'])
        return values
    except Exception, e:
        logger.error('Error retrieving disks usage: %s' % e)
        return False


def get_swapdisk_usage():
    try:
        mem = psutil.swap_memory()
        values = {'total': mem.total,
                  'used': mem.used,
                  'free': mem.free,
                  'sin': mem.sin,
                  'sout': mem.sout,
                  'percent': 100 / float(mem.total) * float(mem.used),
                  }
        return values
    except Exception, e:
        logger.error('Error retrieving swap disk usage: %s' % e)
        return False


def get_disks_io():
    try:
        disks_io = []
        for k, v in psutil.disk_io_counters(perdisk=True).items():
            values = {'device': k,
                      'read_time': v._asdict()['read_time'],
                      'write_bytes': v._asdict()['write_bytes'],
                      'read_bytes': v._asdict()['read_bytes'],
                      'write_time': v._asdict()['write_time'],
                      'read_count': v._asdict()['read_count'],
                      'write_count': v._asdict()['write_count']
                      }
            disks_io.append(values)
        return disks_io
    except Exception, e:
        logger.error('Error retrieving disks IO rates: %s' % e)
        return False


def get_network_io():
    try:
        values = dict(psutil.net_io_counters()._asdict())
        return values
    except Exception, e:
        logger.error('Error retrieving Network IO rates: %s' % e)
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
