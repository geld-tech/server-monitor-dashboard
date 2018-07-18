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
        self.connect_db(self.db_path)
        while True:
            print server.poll_metrics()
            time.sleep(10)

    def stop(self):
        self.disconnect_db()

    def connect_db(self, db_path):
        if os.path.exists(db_path):
            self.db_conn = sqlite3.connect(db_path)
        else:
            self.db_conn = sqlite3.connect(db_path)
            self.db_conn.execute('CREATE TABLE server_metrics(hostname TEXT, cpu_temp TEXT, cpu_percent TEXT)')

    def disconnect_db(self):
        if self.db_conn:
            self.db_conn.close()

# Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        pid_file = '/var/run/monitor-collectord.pid'
        if 'status' == sys.argv[1]:
            try:
                with file(pid_file, 'r') as pf:
                    pid = int(pf.read().strip())
            except IOError:
                pid = None
            except SystemExit:
                pid = None

            if pid:
                print '%s is running as pid %s' % (sys.argv[0], pid)
            else:
                print '%s is not running.' % sys.argv[0]

        else:
            collector = MetricsCollector(pid_file)
            daemon = runner.DaemonRunner(collector)
            daemon.do_action()  # start|stop|restart as sys.argv[1
            sys.exit(0)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
else:
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
