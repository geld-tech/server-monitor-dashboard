#!/usr/bin/env python
import atexit
from daemon import runner
import datetime
import sys
import time
from modules.ServerMetrics import ServerMetrics
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = None


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250), nullable=False)


class SystemInformation(Base):
    __tablename__ = 'system_information'
    id = Column(Integer, primary_key=True)
    platform = Column(String(250))
    system = Column(String(128))
    release = Column(String(128), nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class SystemStatus(Base):
    __tablename__ = 'system_status'
    id = Column(Integer, primary_key=True)
    cpu_percent = Column(Float)
    vmem_percent = Column(Float)
    cpu_temp = Column(Float)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class Process(Base):
    __tablename__ = 'processes'
    id = Column(Integer, primary_key=True)
    pid = Column(String(16))
    name = Column(String(1024))
    cpu_percent = Column(Float)
    date_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship(Server)


class MetricsCollector():
    def __init__(self, pid_file, session):
        self.pidfile_path = pid_file
        self.db_session = session
        self.server = None

        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_timeout = 5
        self.db_path = '/dev/shm/monitor-collectord.sqlite3'
        self.db_conn = None

        atexit.register(self.stop)

    def run(self):
        server = ServerMetrics()
        data = server.poll_metrics()
        self.server = Server(hostname=data['hostname'])
        self.store_system_information(data)
        while True:
            data = server.poll_metrics()
            self.store_system_status(data)
            self.store_processes(data)
            time.sleep(POLL_INTERVAL)

    def stop(self):
        self.db_session.close()

    def disconnect_db(self):
        if self.db_session:
            self.db_session.close()

    def rollback(self):
        self.db_session.rollback()

    def store_system_information(self, data):
        sys_info = SystemInformation(platform=data['platform'], system=data['system'], release=data['release'], server=self.server)
        self.db_session.add(sys_info)
        self.db_session.commit()

    def store_system_status(self, data):
        sys_status = SystemStatus(cpu_percent=data['cpu_percent'], vmem_percent=data['vmem_percent'], cpu_temp=data['cpu_temp'], server=self.server)
        self.db_session.add(sys_status)
        self.db_session.commit()

    def store_processes(self, data):
        for proc in data['processes']:
            if proc['cpu_percent'] > 0.9:  # Won't store unhelpful information
                process = Process(pid=proc['pid'], name=proc['name'], cpu_percent=proc['cpu_percent'], server=self.server)
                self.db_session.add(process)
                self.db_session.commit()


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
PID_FILE = '/tmp/monitor-collectord.pid'
SQLITE_FILE = '/dev/shm/monitor-collectord.sqlite3'
POLL_INTERVAL = 10

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
            engine = create_engine('sqlite:///'+SQLITE_FILE)
            Base.metadata.create_all(engine)
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            collector = MetricsCollector(PID_FILE, session)
            daemon = runner.DaemonRunner(collector)
            daemon.do_action()  # start|stop|restart as sys.argv[1]

            sys.exit(0)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
else:
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
