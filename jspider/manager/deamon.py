# coding:utf-8
from __future__ import absolute_import, unicode_literals
import sys, os, time, atexit
from signal import SIGTERM
import psutil
import yaml

__author__ = "golden"
__date__ = '2017/2/21'


class Daemon(object):
    """
    基本的守护进程类

    使用方法: 继承然后该写run 函数
    """

    def __init__(self, pid_file, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stdout
        self.pid_file = pid_file
        self._pid = None

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        os.chdir("/")
        os.umask(0)
        os.setsid()
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', buffering=1)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.remove_pid_file)
        pid = os.getpid()
        self.pid = pid
        self.write_pid_file()

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        self._pid = value

    def write_pid_file(self):
        # yaml.dump_all([self.pid], open(self.pid_file, 'w'), canonical=False, default_flow_style=False)
        open(self.pidfile, b'w+').write(b"%s\n" % self.pid)

    def remove_pid_file(self):
        os.remove(self.pid_file)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pid_file to see if the daemon already runs
        try:

            pids = yaml.load(open(self.pid_file, 'r+'))
        except IOError:
            pids = {}

        if pids:
            message = "pid_file %s already exist. Daemon already running?%s\n"
            sys.stderr.write(message % (self.pid_file, pids))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()
        return "start success.run as pid %s" % pid

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pid_file
        try:
            pf = open(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pid_file %s does not exist. Daemon not running?\n"
            return message % self.pid_file
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                return 'stop success.pid %s is killed' % pid
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                return 'stop success.pid %s is killed' % pid
            else:
                return err
        finally:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
                return 'stop success.pid %s is killed' % pid

    def restart(self):
        """
        重启
        """
        msg = ''
        msg += self.stop() + '\n'
        time.sleep(2)
        msg += self.start()
        return msg

    def run(self):
        """
        运行的代码
        """
        pass

    def status(self):
        if self.is_running:
            return "is running as pid %s" % self.pid
        else:
            return "is not running"

    @property
    def is_running(self):
        if self.pid:
            ps = psutil.Process(self.pid)
            if ps and ps.is_running() and ps.status() != "zombie":
                return True
        return False


