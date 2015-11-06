#!/usr/bin/env python

import os
import subprocess as sp

from munin import MuninPlugin

class LsofCount(MuninPlugin):
	title = "Number of open files (Varnish)"
        args = "--base 1000 -l 0"
        vlabel = "open_files"
        scaled = False
        category = "varnish"

        @property
        def fields(self):
                warning = os.environ.get('lsof_warn', 80000)
                critical = os.environ.get('lsof_crit', 90000)
                return [("lsof", dict(
                        label = "lsof",
                        info = 'The number of open files',
                        type = "GAUGE",
                        min = "0",
                        warning = str(warning),
                        critical = str(critical)))]

        def execute(self):
		pid_of_varnish = int(sp.check_output("ps auxww | grep nobody | grep varnishd | grep -v grep | awk '{ print $2 }'", shell=True))
		# print (pid_of_varnish)
                _fd_count = int(sp.check_output("ls -al /proc/" + str(pid_of_varnish) + "/fd/ 2>&1 | grep -v directory | wc -l", shell=True))
                print ("lsof.value %s" % _fd_count)

if __name__ == "__main__":
	LsofCount().run()

