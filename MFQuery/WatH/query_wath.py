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

import argparse
import sys
from siphon.catalog import TDSCatalog
from siphon.ncss import NCSS
from MFQuery.MF.helpers import *
import MFQuery.MF.MF as MF  
# import the dictionaries describing the metadata associated with the directory structure and the experiment
from MFQuery.data import wath_meta


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
    parser.add_argument('-y','--year', type=str, nargs="*", help='Year indicating experiment', required=False)
    parser.add_argument('-s','--sst', type=str, nargs="*", help='CMIP5 model used to calculate delta-sst'+
           ' Can be "None"', required=False)
    parser.add_argument('-f','--forcing', type=str, help='NAT or ALL forcing', required=False)
    parser.add_argument('-m','--meta', type=str, nargs="*", 
                        help='''generic metadata argument: -m/--meta argument-name argument value
                        for a full list of available metadata use the -pm flag''', required=False)
    parser.add_argument('-d','--download', help='download files returned by query', action='store_true', required=False)
    parser.add_argument('-p','--download_path', type=str, help='Define local path where to download files,' +
                                                'if not defined will use current path', required=False)
    parser.add_argument('-o','--opendap', help='print thredds opendap urls for files returned by query',
                                          action='store_true', required=False)
    parser.add_argument('-n','--ncss', help='print thredds netcdf subset service urls for files returned by query',
                                       action='store_true', required=False)
    parser.add_argument('-v','--variable', type=str, nargs="*", help='variable', required=False)
    parser.add_argument('-k','--output_kind', type=str, nargs="*", help='pcl, pdl or pel', required=False)
    parser.add_argument('-pm','--print_meta', help='print metadata documents and exit', required=False,
                        action='store_true')
    parser.add_argument('-a','--admin', action='store_true', help='running script as admin', required=False)
    args = parser.parse_args()
    print(args)
    if not args.print_meta and args.year is None:
        parser.error('Argument year  -y/--year is required to query the data')
    else:
        return vars(args)


def assign_constraints():
    ''' Assign default values and input to constraints '''
    kwargs = parse_input()
    print(kwargs)
    # if print_meta option True print metadata definitions and exit
    if kwargs.pop('print_meta'):
        print_meta(wath_meta)
        sys.exit()
    admin =  kwargs.pop("admin")
    out_args, kwargs = output_args(kwargs)
    # build separate boolean arguments from meta option
    extra_args = meta_arguments(kwargs.pop("meta"), wath_meta)
    kwargs.update(extra_args)
    # if sst and year have only one value convert list to string
    for k in ['sst','year']:
        if len(kwargs[k]) == 1 : kwargs[k] = kwargs[k][0]  
    # copy remaining arguments and eliminate the ones which are empty or None
    for k,v in list(kwargs.items()):
        if v is None or v==[]: kwargs.pop(k)
    return kwargs, out_args, admin


def output_args(kwargs):
    ''' collect all input arguments related to output format in separate dictionary '''
    args={}
    args['opendap'] = kwargs.pop("opendap")
    args['ncss'] = kwargs.pop("ncss")
    args['variable'] = kwargs.pop("variable")
    args['output_kind'] = kwargs.pop("output_kind")
    args['download'] = kwargs.pop("download")
    args['download_path'] = kwargs.pop("download_path")
    return args, kwargs


def query_mf(query,template):
    ''' query mediaflux using input arguments and selected output template '''
    results={}
    return results


def build_query(kwargs):
    ''' build bulk of query string based on input arguments '''
    print(kwargs)
    query = '''asset.query :where "namespace>='/WatH-Test/model_output2/' and '''
    # define MF metadata namespace containing metadata documents
    namespace = "weather_at_home"
    for k,v in kwargs.items():
        meta_doc = wath_meta[k][2]
        if type(v) == str:
            query += namespace + ":" + meta_doc + "/" + k + "='" + v + "' and "
        elif type(v) == bool:
            query += namespace + ":" + meta_doc + "/" + k + "=" + str(v) + " and "
        elif type(v) == list:
            query += "("
            for value in v:
                query += \
                namespace + ":" + meta_doc + "/" + k + "='" + value + "' or "
            query = query[:-4] + ") and "
   # xpath(weather_at_home:drs_meta/volunteer)
    # return query without last for characters so we don't return the last "and "
    print(query)
    return query[:-4]+ '"'


#def build_action(out_args):
#    ''' build action to perform on results returned by query '''
#    opendap_urls = ''' :action get-distinct-values :xpath -ename url string.format('https://thredds.com.au%s?',''' +
#                   '''replace(xvalue('namespace'),'/WatH-Test/model_output2','')) '''
#    download_urls = ''' :action get-distinct-values :xpath -ename '''
#    count = ''' :action count '''


def process_output():
    pass
    return


def tds_connect():
    ''' open connection to thredds catalog, return datasets list '''
    global tds, xml_suf
    cat = TDSCatalog(tds + 'aggregated' + xml_suf)
    return list(cat.datasets.values())


def main():
    ''' '''
    global tds, xml_suf
    # parse input arguments 
    query_args, out_args, admin = assign_constraints()
    print(out_args)
    # thredds root url
    tds = 'http://144.6.229.249/thredds/catalog/'
    html_suf = '/catalog.html'
    xml_suf = '/catalog.xml'
    # establish session 
    session = MF.connect()
    # build query and then call MF.query to execute
    squery = build_query(query_args)
    #saction = ""
    #saction = 'count'
    saction = '''get-distinct-values :xpath -ename url''' +\
              ''' "replace(xvalue('namespace'),'/WatH-Test/model_output2/','')"'''
    output = session.query(squery,action=saction)
    # get possible combinations of 'year' and 'sst'
    # build one query for each of the year/sst combinations


    # do something with result!
    # open file?
    lname_dict = {'pcl': '/global_monthly_mean_diagnostic_',
                  'pdl': '/regional_daily_mean_diagnostic_',
                  'pel': '/regional_monthly_mean_diagnostic_'}
    if out_args['opendap'] or out_args['ncss']:
       urls_list = []
       if out_args['output_kind']:
           tail = [lname_dict[x] for x in out_args['output_kind']]
       else:
           tail = [html_suf]
       # dataset = tds_connect()
       for y in tail:
           urls_list.extend( [tds + 'aggregated/' + x + y for x in session.response(output,saction) ] )
       for url in urls_list:
           if url[-1] == "_": print( url + url.split("/")[-2] + ".nc" )
            # http://144.6.229.249/thredds/dodsC/aggregated/2013/NAT/HadGEM2-ES/dir00001/n783/n783.pel.ncml.html
            # http://144.6.229.249/thredds/catalog/aggregated/2013/NAT/HadGEM2-ES/dir00001/n783/catalog.html?dataset=WathAggregated/2013/NAT/HadGEM2-ES/dir00001/n783/n783.pel.ncml
    print(urls_list)
if __name__ == "__main__":
    main()
