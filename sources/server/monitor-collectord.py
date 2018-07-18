#!/usr/bin/env python
import atexit
from daemon import runner
import os
import sqlite3
import sys
import time

from ServerMetrics import ServerMetrics


class MetricsCollector():
    def __init__(self, pid_file):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = pid_file
        self.pidfile_timeout = 5
        self.db_path = '/dev/shm/server-metrics.sqlite3'
        self.db_conn = None

        atexit.register(self.stop)

    def run(self):
        server = ServerMetrics()
        data = server.poll_metrics()
        self.connect_db(self.db_path)
        self.store_system_information(data)
        while True:
            data = server.poll_metrics()
            self.store_system_status(data)
            self.store_processes(data)
            time.sleep(10)

    def stop(self):
        self.disconnect_db()

    def connect_db(self, db_path):
        if os.path.exists(db_path):
            self.db_conn = sqlite3.connect(db_path)
        else:
            self.db_conn = sqlite3.connect(db_path)
            self.db_conn.execute('''CREATE TABLE system_information(
                                    hostname TEXT,
                                    architecture TEXT,
                                    platform TEXT,
                                    system TEXT,
                                    release TEXT)''')
            self.db_conn.execute('''CREATE TABLE system_status(
                                    hostname TEXT,
                                    temperature TEXT,
                                    uptime TEXT,
                                    cpu_percent TEXT,
                                    mem_percent TEXT,
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            self.db_conn.execute('''CREATE TABLE processes(
                                    pid TEXT,
                                    name TEXT,
                                    cpu_percent TEXT,
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            self.db_conn.commit()

    def disconnect_db(self):
        if self.db_conn:
            self.db_conn.close()

    def store_system_information(self, data):
        self.db_conn.execute('INSERT INTO system_information(hostname, architecture, platform, system, release) VALUES ("%s", "%s", "%s", "%s", "%s")'
                             % (data['hostname'], data['architecture'], data['platform'], data['system'], data['release']))
        self.db_conn.commit()

    def store_system_status(self, data):
        self.db_conn.execute('INSERT INTO system_status(hostname, temperature, uptime, cpu_percent, mem_percent) VALUES ("%s", "%s", "%s", "%s", "%s")'
                             % (data['hostname'], data['cpu_temp'], data['uptime'], data['cpu_percent'], data['vmem_percent']))
        self.db_conn.commit()

    def store_processes(self, data):
        for proc in data['processes']:
            if proc['cpu_percent'] > 0.1:
                self.db_conn.execute('INSERT INTO processes(pid, name, cpu_percent) VALUES ("%s", "%s", "%s")'
                                     % (proc['pid'], proc['name'], proc['cpu_percent']))
                self.db_conn.commit()


def is_running(pid_file):
    try:
        with file(pid_file, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None
    except SystemExit:
        pid = None

    if pid:
        return True, pid
    else:
        return False, -1


# Main
PID_FILE = '/var/run/monitor-collectord.pid'

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if 'status' == sys.argv[1]:
            running, pid = is_running(PID_FILE)
            if running:
                print '%s is running as pid %s' % (sys.argv[0], pid)
            else:
                print '%s is not running.' % sys.argv[0]
        elif 'stop' == sys.argv[1] and not is_running(PID_FILE)[0]:
            print '%s is not running.' % sys.argv[0]
        else:
            collector = MetricsCollector(PID_FILE)
            daemon = runner.DaemonRunner(collector)
            daemon.do_action()  # start|stop|restart as sys.argv[1
            sys.exit(0)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
else:
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
