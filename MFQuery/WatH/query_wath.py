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
import sys
from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS 

from MFQuery.MF.helpers import *
import MFQuery.MF.MF  
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
             -- the netcdf subset service urls of the search results in a file
             -- donwload the simulations to the current directory 
             -- a python list with the simulations opendap urls (if used in interactive mode)
             The arguments year, sst and ..  can be repeated, for
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
    parser.add_argument('-y','--year', type=str, nargs="*", help='Year indicating experiment', required=True)
    parser.add_argument('-s','--sst', type=str, nargs="*", help='CMIP5 model used to calculate delta-sst'+
           ' Can be "None"', required=False)
    parser.add_argument('-f','--forcing', type=str, help='NAT or ALL forcing', required=False)
    parser.add_argument('-m','--meta', type=str, nargs="*", 
                        help='''generic metadata argument: -m/--meta argument-name argument value
                        for a full list of available metadata use the -pm flag''', required=False)
    parser.add_argument('-d','--download', help='download files returned by query', action='store_true', required=False)
    parser.add_argument('-p','--download_path', type=str, help='Define local path where to download files, if not defined will use current path', required=False)
    parser.add_argument('-o','--opendap', help='print thredds opendap urls for files returned by query', action='store_true', required=False)
    parser.add_argument('-n','--ncss', help='print thredds netcdf subset service urls for files returned by query', action='store_true', required=False)
    parser.add_argument('-v','--variable', type=str, nargs="*", help='variable', required=False)
    parser.add_argument('-k','--output_kind', type=str, nargs="*", help='pcl, pdl or pel', required=False)
    parser.add_argument('-pm','--print_meta', help='print metadata documents and exit', action='store_true', required=False)
    parser.add_argument('-a','--admin', action='store_true', help='running script as admin', required=False)
    return vars(parser.parse_args())


def assign_constraints():
    ''' Assign default values and input to constraints '''
    kwargs = parse_input()
    admin =  kwargs.pop("admin")
    # collect all input arguments related to output format in separate dictionary
    out_args={}
    out_args['opendap'] = kwargs.pop("opendap")
    out_args['ncss'] = kwargs.pop("opendap")
    out_args['variable'] = kwargs.pop("variable")
    out_args['output_kind'] = kwargs.pop("output_kind")
    out_args['download'] = kwargs.pop("download")
    out_args['download_path'] = kwargs.pop("download_path")
    out_args['print_meta'] = kwargs.pop("print_meta")
    # collect all boolean arguments separately
    extra_args = meta_arguments(kwargs.pop("meta"))
    
    # copy remaining arguments and eliminate the ones which are empty or None
    for k,v in list(kwargs.items()):
        if v is None or v==[]: kwargs.pop(k)
    return kwargs, extra_args, out_args, admin


def query_mf(query,template):
    ''' query mediaflux using input arguments and selected output template '''
    results={}
    return results

def build_query(kwargs):
    ''' build bulk of query string based on input arguments '''
    query = '''asset.query :where "namespace>='/WatH-Test/model_output/2013/NAT/HadGEM2-ES' and ''' 
    # define MF metadata namespace containing metadata documents
    namespace = "weather_at_home"
    for k,v in kwargs.items():
        if k in drs_meta.keys():
            meta_doc = "drs_meta"
        else:
            meta_doc = "experiment_description"
        value=str(v)
        query += namespace + ":" + meta_doc + "/" + k + "=" + "'" + value + "' and "
   # xpath(weather_at_home:drs_meta/volunteer)
    # return query without last for characters so we don't return the last "and "
    print(query)
    return query[:-4]+ '"'


def build_action(out_args):
    ''' build action to perform on results returned by query '''
    opendap_urls = ''' :action get-distinct-values :xpath -ename url string.format('https://thredds.com.au%s?',replace(xvalue('namespace'),'/WatH-Test/model_output2','')) '''
    download_urls = ''' :action get-distinct-values :xpath -ename '''
    count = ''' :action count '''


def process_output():
    base = ( '''asset.query :where "namespace>=/WatH-Test/model_output2 '''
             '''and type='application/x-netcdf' and QUERY ''' 
             ''' :action get-distinct-values ''' )
    thredds_out = ( ''' :xpath -ename url string.format('https://http://144.6.229.249/thredds/catalog/my/test/all2%s?','''
                     ''',replace(xvalue('namespace'),'/WatH-Test/model_output2',''))''' )
    base2 =  ''' curl --insecure -X POST -H 'Content-Type: text/xml; charset=utf-8' -d '<request><service name="asset.query" session="15bf0af565bbGXRL1cTxXXoqHKmlwXfGBUNZGo69yLk"><args><where>namespace>=/WatH-Test/model_output2 and type='application/x-netcdf' and (YOUR_QUERY)</where><action>get-distinct-values</action><xpath name="url">string.format('https://thredds.com.au%s?',replace(xvalue('namespace'),'/WatH-Test/model_output2',''))</xpath></args></service></request>' 'https://livearc-00.tpac.org.au/__mflux_svc__' " '''
    return base


def tds_connect():
    ''' open connection to thredds catalog, return datasets list '''
    cat = TDSCatalog('http://144.6.229.249/thredds/catalog/wath2/2012/NAT/HadGEM2-ES/dir001/p2ofga/catalog.xml')
    return list(cat.datasets.values())


def main():
    ''' '''
    # parse input arguments 
    query_args, bool_args, out_args, admin = assign_constraints()
    # if user wants to print metadata definition, print and exit 
    if out_args['print_meta']: 
        print_meta(drs_meta)
        print_meta(experiment_meta)
        sys.exit()
    print(out_args)
    # establish session 
    session = MF.connect()
    # build query and then call MF.query to execute
    squery = build_query(query_args)
    squery += MF.action('count')
    output = MF.query(squery)
    print(output)
    sys.exit()
    results = process_output(out_args)
    # get possible combinations of 'year' and 'sst'
    # build one query for each of the year/sst combinations 
    print(query_args)
    print(bool_args)

    combs=combine_constraints(**query_args)
    
    print(combs)
    for constraints in combs:
        print(constraints.update(bool_args))
        query = build_query(constraints)
        # query mediaflux
        result_dict = query_mf(query,template)
        print(result_dict)
    # do something with result!
    # open file?
    if opendap or ncss:
        dataset = tds_connect()

if __name__ == "__main__":
    main()
