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

from __future__ import print_function

import itertools

def combine_constraints(**kwargs):
    ''' Works out any possible combination given lists of constraints
        :argument dictionary, keys are fields and values are lists of values for each field
        :return: a set of dictionaries, one for each constraints combination i
    '''
    try:
        return [dict(itertools.izip(kwargs, x)) for x in itertools.product(*kwargs.itervalues())]
    except:
        return [dict(zip(kwargs, x)) for x in itertools.product(*kwargs.values())]


def print_meta(meta_dict):
    ''' print a metadata document dictionary in a readable form '''
    for k,v in meta_dict.items():
        print()
        print (k)
        print ('type: ',v[0])
        print ('summary: ',v[1])
    return


def meta_arguments(args_list):
    ''' gets a list of metadata arguments as [arg1, value1, arg2, value2, arg3, value3] '''
    args_dict = {}
    # use eval_bool function to assign correct type to boolean values
    args = [ eval_bool(i) for i in args_list]
    for i in range(0,len(args),2):
        args_dict[args[i]] = args[i+1]
    return args_dict


def eval_bool(bool_str):
    ''' Get a string if represents a boolean convert it to bool type '''
    if bool_str in ["1","T", "True","true","Y","y","yes","Yes","YES","TRUE"]:
        return True
    elif bool_str in ["0","F", "False","false","N","n","no","No","NO","FALSE"]:
        return False
    else:
        return bool_str
