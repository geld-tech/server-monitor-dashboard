#!/usr/bin/env python
import sys
import time
from daemon import runner


class MetricsCollector():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/monitor-collectord.pid'
        self.pidfile_timeout = 5
    def run(self):
        while True:
            print 'Running..'
            time.sleep(10)


# Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        collector = MetricsCollector()
        daemon = runner.DaemonRunner(collector)
        daemon.do_action() # start|stop|restart as sys.argv[1
        sys.exit(0)
    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
else:                                                           
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
