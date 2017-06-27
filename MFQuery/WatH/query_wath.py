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

import argparse
# import the dictionaries describing the metadata associated with the directory structure and the experiment
from MFQuery.data import drs_meta, experiment_meta


def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description=r''' Query the Weather@Home collection
             on the TPAC mediaflux server, matching the constraints
             passed as arguments.
             The script prints a summary of the search results, then gives an option to choose between
             the following outputs:
             -- the opendap urls of the search results in a file
             -- donwload the simulations to the current directory 
             -- a python list with the simulations opendap urls (if used in interactive mode)
             The arguments year, sst_model and ..  can be repeated, for
            example to select two sst-model:
            -m HadGEM2-ES MMM          NB (MMM is the MultiModel Mean)
            At least one experiment/year should be passed all other arguments are optional.
            The script returns all the ensembles satifying the constraints
            [year1 OR year2 OR ..] AND [GHG True] AND [sst-model1 OR sst-model2 OR ...]
            AND [ALL-forcing]
            Frequency adds all the correspondent mip_tables to the mip_table list.
            If a constraint isn't specified for one of the fields automatically all values
            for that field will be selected.
            The additional arguments replica, node and project modify the main ESGF search parameters. Defaults are
            no replicas, PCMDI node and CMIP5 project. If you chnage project you need to export a different local database,
               ''',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a','--admin', action='store_true', default=False, help='running script as admin', required=False)
    parser.add_argument('-y','--year', type=str, nargs="*", help='Year indicating experiment', required=True)
    parser.add_argument('-m','--sst_model', type=str, nargs="*", help='CMIP5 model used to calculate delta-sst'+
           ' Can be "None"', required=False)
    parser.add_argument('-f','--forcing', type=str, help='NAT or ALL forcing', required=False)
    parser.add_argument('-g','--ghg', type=str, help='simulation with GHG, is True or False', required=False)
    parser.add_argument('-w','--wind_rh', type=str, help='simulation with WIND-RH, is True or False', required=False)
    parser.add_argument('-fi','--fire_index', type=str, help='simulation with FFDI, is True or False', required=False)
    parser.add_argument('-k','--keyword', type=str, nargs="*", help='extra keyword to be look for in description', required=False)
    parser.add_argument('-v','--variable', type=str, nargs="*", help='variable', required=False)
    parser.add_argument('-ok','--output_kind', type=str, nargs="*", help='pcl, pdl or pel', required=False)
    parser.add_argument('-o','--opendap', help='search also replica', action='store_true', required=False)
    parser.add_argument('-d','--download', type=str, help='ESGF node to use for search', required=False)
    parser.add_argument('-p','--download_path', type=str, help='ESGF project to search', required=False)
    return vars(parser.parse_args())
    return kwargs


def assign_constraints():
    ''' Assign default values and input to constraints '''
    kwargs = parse_input()
    out_args={}
    out_args['opendap'] = kwargs.pop("opendap")
    out_args['variable'] = kwargs.pop("variable")
    out_args['output_kind'] = kwargs.pop("output_kind")
    out_args['download'] = kwargs.pop("download")
    out_args['download_path'] = kwargs.pop("download_path")
    searchargs['node'] = kwargs.pop("node")
    for k,v in list(kwargs.items()):
        if v is None or v==[]: newkwargs.pop(k)
    for k,v in list(searchargs.items()):
        if v is None or v==[]: searchargs.pop(k)
    return newkwargs, out_args


def experiment_description():
    ''' import definition of weather_at_home:experiment_description metadata document '''
    return


def query_mf(kwargs):
    ''' query mediaflux using input arguments '''
    results={}
    query="WHERE"
    pass
    return results


def main():
    ''' '''
    
    # parse input arguments 
    kwargs, out_args = assign_constraints()
    # query mediaflux
    result_dict = query_mf(kwargs)
    print(result_dict)
    # do something with result!
    # open file?

