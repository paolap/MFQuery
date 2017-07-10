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

import pytest


@pytest.fixture(scope="module")
def aterm_files():
    cfg_path='/User/tizio/aterm.cfg'
    jar_path = '/User/tizio/aterm.jar'
    return (cfg_path, jar_path)


@pytest.fixture(scope="module")
def metadata():
    metadata = {'meta1': ['bool', 'description1', 'doc1'],
                'meta2': ['string', 'description2', 'doc2'],
                'meta3': ['bool', 'description3', 'doc2'],
                'meta4': ['string', 'description4', 'doc2']
                }
    return metadata


@pytest.fixture(scope="module")
def args_list():
    args_list = ['meta1', 'True', 'meta2', '1', 'meta3', 'F', 'meta4', '987']
    return args_list

