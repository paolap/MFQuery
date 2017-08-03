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

from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS


def tds_connect(tds):
    """
    :return: datasets list after opening connection to Thredds catalogue
    """
    cat = TDSCatalog(tds + 'aggregated' + xml_suf)
    return list(cat.datasets.values())


def ncss_subset(tds):

    ds_list = tds_connect(tds)
    dset1 = ds_list[0]
    ncss_obj = NCSS(dset1.access_urls['NetcdfSubset'])
    subset = ncss_obj.query()
    subset.lonlat_box(142, 149, -45, -38)
    subset.accept('netcdf')
    subset.variables('tasmax', 'tasmin')
    #data = ncss.get_data(subset)
    return subset
