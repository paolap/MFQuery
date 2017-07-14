# This collects all other helper functions 
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

import sys


def print_meta(meta_dict):
    ''' print a metadata document dictionary in a readable form '''
    for k,v in sorted(meta_dict.items()):
        print()
        print (k)
        print ('type:', v[0])
        print ('summary:', v[1])
        print ('document:', v[2])
    return


def meta_arguments(args_list, meta_dict):
    ''' gets a list of metadata arguments as [arg1, value1, arg2, value2, arg3, value3] '''
    args_dict = {}
    for i in range(0, len(args_list),2):
        args_dict[args_list[i]] = args_list[i+1]
    # use eval_bool function to assign correct type to boolean values
    for k,v in args_dict.items():
        if meta_dict[k][0] == 'bool': args_dict[k] = eval_bool(v)

    return args_dict


def eval_bool(bool_str):
    ''' Get a string if represents a boolean convert it to bool type '''
    if bool_str.lower() in ["1","t","true","y","yes"]:
        return True
    elif bool_str.lower() in ["0","f", "false", "n","no"]:
        return False
    else:
        print('Boolean value expected, found ', bool_str)
        sys.exit()

def res_list(response):
    ''' 
    :param response: a response string from the MF server
    :return: a list of tuples containing substring value and kind as element key, subkey or value)
    '''
    res=[]
    for s in response.split():
        if s[0] == ":":
            res.append((s[1:],'key'))
        elif s[0] == "-":
            res.append((s[1:], 'subkey'))
        else:
            res.append((s.replace('"',''), 'value'))
    return res

def res_dict(res):
    '''
    :param res: MF server response as list as generated by res_list()
    :return: a dictionary representing response in a json-like format
    '''
    d = {}
    subkey = None
    if res[0][1] != 'key':
        print('all responses should start with a key')
        print(response)
        sys.exit()
    else:
        lastkey = res[0][0]
        d[lastkey] = []
    for tup in res[1:]:
        if tup[1] == 'key':
            lastkey = tup[0]
            d[lastkey]= []
            subkey = None
        elif tup[1] == 'subkey':
            subkey = tup[0]
            d[lastkey].append({tup[0]: []})
        elif tup[1] == 'value':
            if subkey:
                d[lastkey][-1][subkey].append(tup[0])
            else:
                d[lastkey].append(tup[0])
    return d