#!/usr/bin/env python
"""
Copyright 2017 ARC Centre of Excellence for Climate Systems Science
author: Paola Petrelli <paola.petrelli@utas.edu.au>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function
import os
import subprocess


class Session(object):

    def open(self, cfg_file, jar_file):
        ''' open a Mediaflux session using the token '''
        self.cfg_file = cfg_file
        self.jar_file = jar_file 
        return self

    def query(self, squery):
        ''' execute query passed as input '''
        script = self.wrapper(squery)
        out = self.execute(script)
        result = self.parse_response(out)
        return result

    def wrapper(self, cmd):
        ''' create a java script wrapper for query command '''
        script = 'java -Dmf.cfg={0} -jar {1} nogui {2} '.format(self.cfg_file, self.jar_file, cmd)
        return script

    def execute(self,script):
        ''' execute java script '''
        print("exec: {0}".format(script))
# CURRENT - for security reasons, shell=True should not be set
# CURRENT - the shlex approach works on unix, but not on windows ...
#       proc = subprocess.Popen(shlex.split(script), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        stdout = stdout.rstrip("\n")
        stderr = stderr.rstrip("\n")
# CURRENT - JAVA prints "Picking up env var crap" here to stderr ...
# so we cannot use the existence of stderr as an indication of a problem - must fall to the parsing of stdout
        if (stderr):
                log("DEBUG", stderr)
                if not "JAVA" in stderr:
                        raise Exception("Process execution failed.")
        return stdout

        def parse_response(self, response):
            ''' parse response returned by server to a dictionary '''
            resp_dict=response
            return resp_dict

def actions(value):
    ''' attach an :action to a query before execution '''
    action = ' :action ' + value
    return action


def connect(cfg = None , jar = None):
    """ Connect to MF using a token with authority to access the data collection

    :return: A new :py:class:`Session`

    Example::

    >>> from MFQuery import WatH
    >>> cfg = "$HOME/aterm.cfg"
    >>> jar = "$HOME/aterm.jar"
    >>> wath   = WatH.MF.connect(cfg,jar) # doctest: +SKIP
    >>> outputs = wath.query() # doctest: +SKIP
    """

    # if user didn't pass configuration and jar file assume their in $HOME
    if cfg is None:
        cfg = os.environ.get('ATERMCFG', "$HOME/aterm.cfg")
    if jar is None:
        jar = os.environ.get('ATERMJAR', "$HOME/aterm.jar")

    session = Session()
    session.open(cfg, jar)
    return session

