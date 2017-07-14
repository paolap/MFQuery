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
import pytest


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


def test_eval_bool(capsys):
    assert helpers.eval_bool('T') == True
    assert helpers.eval_bool('0') == False
    assert helpers.eval_bool('TrUe') == True
    assert helpers.eval_bool('NO') == False
    with pytest.raises(SystemExit):
        helpers.eval_bool('notincluded')
        out, err = capsys.readouterr()
        assert out=='Boolean value expected, found notincluded'


def test_res_list():
    res = ''':key1 -sub1 val1 :key2 "val2" "val3" '''
    assert helpers.res_list(res) == [("key1", "key"), ("sub1","subkey"), ("val1","value"),
                             ("key2", "key"), ("val2", "value"), ("val3", "value")]


def test_res_dict():
    # one key with one value
    key_value = [("key1", "key"), ("val1", "value")]
    assert helpers.res_dict(key_value) == {"key1": ["val1"]}
    # one key with more than one value
    key_values = [("key1", "key"), ("val1", "value"), ("val2", "value")]
    assert helpers.res_dict(key_values) == {"key1": ["val1", "val2"]}
    # more than one key with 1 value each
    keys_value = [("key1", "key"), ("val1", "value"), ("key2", "key"), ("val2", "value")]
    assert helpers.res_dict(keys_value) == {"key1": ["val1"], "key2": ["val2"]}
    # more than one key with more than one value
    keys_values = [("key1", "key"), ("val1", "value"), ("val3", "value"),
                   ("key2", "key"), ("val2", "value"), ("val4", "value")]
    assert helpers.res_dict(keys_values) == {"key1": ["val1", "val3"], "key2": ["val2", "val4"]}
    # one key with one subkey with one value
    key_subkey_value = [("key1", "key"), ("sub1", "subkey"), ("val1", "value")]
    assert helpers.res_dict(key_subkey_value) == {"key1": [{"sub1": ["val1"]}]}
    # more than one key with one subkey with one value
    keys_subkey_value = [("key1", "key"), ("sub1", "subkey"), ("val1", "value"),
                         ("key2", "key"), ("sub2", "subkey"), ("val2", "value")]
    assert helpers.res_dict(keys_subkey_value) == {"key1": [{"sub1": ["val1"]}],
                                                   "key2": [{"sub2": ["val2"]}]}
    # complex combination
    res_list = [("key1", "key"), ("sub1", "subkey"), ("val1", "value"),
                  ("key2", "key"), ("val2", "value"), ("val3", "value")]
    assert helpers.res_dict(res_list) == {"key1": [{"sub1": ["val1"]}], "key2": ["val2", "val3"] }