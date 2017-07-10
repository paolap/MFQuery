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

import MFQuery.MF.MF as mf
from tests.MF.mf_fixtures import aterm_files


def test_connect(aterm_files):
    s = mf.connect()
    assert s.cfg_file == '$HOME/aterm.cfg'
    assert s.jar_file == '$HOME/aterm.jar'
    s = mf.connect(cfg=aterm_files[0], jar=aterm_files[1])
    assert s.cfg_file == '/User/tizio/aterm.cfg'
    assert s.jar_file == '/User/tizio/aterm.jar'