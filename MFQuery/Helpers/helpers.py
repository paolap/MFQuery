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
