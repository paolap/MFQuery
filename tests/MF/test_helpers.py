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

import MFQuery.MF.helpers as helpers
from tests.MF.mf_fixtures import metadata, args_list


def test_print_meta(capfd,metadata):
    helpers.print_meta(metadata)
    out, err = capfd.readouterr()
    assert out == '''
meta1
type: bool
summary: description1
document: doc1

meta2
type: string
summary: description2
document: doc2

meta3
type: bool
summary: description3
document: doc2

meta4
type: string
summary: description4
document: doc2
'''

def test_meta_arguments(args_list, metadata):
    args = helpers.meta_arguments(args_list, metadata)
    assert args == {'meta1': True,
                    'meta2': '1',
                    'meta3': False,
                    'meta4': '987' }


def test_eval_bool():
    assert helpers.eval_bool('T') == True
    assert helpers.eval_bool('0') == False
    assert helpers.eval_bool('True') == True
    assert helpers.eval_bool('NO') == False