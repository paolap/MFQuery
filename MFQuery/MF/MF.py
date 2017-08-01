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

from __future__ import print_function, absolute_import

import os
import subprocess
from MFQuery.MF.helpers import res_list, res_dict


class Session(object):

    def open(self, cfg_file, jar_file):
        ''' open a Mediaflux session using the token '''
        self.cfg_file = cfg_file
        self.jar_file = jar_file 
        return self

    def query(self, squery, action=""):
        '''
         :param squery: a query string
         :param action: an action to execute with the query results, default to showing returned assets
         :return server response after executing query '''
        if action == "" or action is None : action = 'count'
        squery += ' :action ' + action
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
        stdout = stdout.decode('utf8').replace("\n","")
        stderr = stderr.decode('utf8').replace("\n","")
        print(stderr)
# CURRENT - JAVA prints "Picking up env var crap" here to stderr ...
# so we cannot use the existence of stderr as an indication of a problem - must fall to the parsing of stdout
        if stderr != "":
#log("DEBUG", stderr)
                if not "JAVA" in stderr:
                        raise Exception("Process execution failed.")
        return stdout

    def parse_response(self, response):
        ''' parse response returned by server to a dictionary '''
# first break string where whitespaces, then create json
# elements start with ":"
# attributes start with "-"
# values are surrounded by double quotes
        response_list = res_list(response)
        response_dict = res_dict(response_list)
        return response_dict


    def response(self, response_dict, action):
        '''
        :param response_dict: dictionary with parsed MF server response
        :param action: a string representing the action executed by the MF server
        :return: response: depending on server action return a simplified version of response
                 if 'count' returns number of results
                 if '' returns a list with assets
                 if 'get-distinct-values' returns list with distinct assets urls
        '''
        kaction=action.split(" ")[0]
        xvalue=""
        if kaction in ['get-value', 'get-distinct-values', 'get-values']:
            xvalue = action.split("-ename ")[1].split(" ")[0]
        action_dict={'count': 'value',
                     'get-id': 'id',
                     'get-distinct-values': 'url',
                     'get-name': 'name',
                     'get-path':  'path',
                     'get-value': xvalue,
                     'get-values': xvalue,
                     'get-distinct-values': xvalue}
        #  get - value, get - values, get - distinct - values, get - content, get - geo - shape,
        # get - geo - histogram, get - transformed, get - content - status - statistics, get - all, pipe, sum, min, max,
        # avg]
        # probably shouldn't be included: get-cid, get-rid, get-path
        # can be included but complex: get-meta, get-template-meta (can't see difference yet), get-extended-meta
        # get-value
        key = action_dict[kaction]
        subdict = [y for y in response_dict if key in y.keys() ]
        response = [x for y in subdict for x in y[key]  if type(x) is str]
        if len(response) == 1: return response[0]
        return response

def connect(cfg = None , jar = None):
    """ Connect to MF using a token with authority to access the data collection

    :return: A new :py:class:`Session`

    Example::

    >>> from MFQuery.MF import MF
    >>> cfg = "$HOME/aterm.cfg"
    >>> jar = "$HOME/aterm.jar"
    >>> wath   = MF.connect(cfg,jar) # doctest: +SKIP
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

