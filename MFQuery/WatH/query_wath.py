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
from MFQuery.MF.ncss_subset import ncss_subset
# import the dictionaries describing the metadata associated with the directory structure and the experiment
from MFQuery.data import wath_meta


def parse_input():
    """
    :return: parsed input
    """
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
            If a constraint isn't specified for one of the fields automatically all values
            for that field will be selected.
               ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-y', '--year', type=str, nargs="*", help='Year indicating experiment', required=False)
    parser.add_argument('-s', '--sst', type=str, nargs="*", help='CMIP5 model used to calculate delta-sst' +
                                                                 ' Can be "None"', required=False)
    parser.add_argument('-f', '--forcing', type=str, help='NAT or ALL forcing', required=False)
    parser.add_argument('-m', '--meta', type=str, nargs="*",
                        help='''generic metadata argument: -m/--meta argument-name argument value
                        for a full list of available metadata use the -pm flag''', required=False)
    parser.add_argument('-d', '--download', help='download files returned by query', action='store_true',
                        required=False)
    parser.add_argument('-p', '--download_path', type=str, help='Define local path where to download files,' +
                                                                'if not defined will use current path', required=False)
    parser.add_argument('-o', '--opendap', help='print thredds opendap urls for files returned by query',
                        action='store_true', required=False)
    parser.add_argument('-n', '--ncss', help='print thredds netcdf subset service urls for files returned by query',
                        action='store_true', required=False)
    parser.add_argument('-v', '--variable', type=str, nargs="*", help='variable', required=False)
    parser.add_argument('-k', '--output_kind', type=str, nargs="*", help='pcl, pdl or pel', required=False)
    parser.add_argument('-pm', '--print_meta', help='print metadata documents and exit', required=False,
                        action='store_true')
    #parser.add_argument('-a', '--admin', action='store_true', help='running script as admin', required=False)
    args = parser.parse_args()
    print(args)
    if not args.print_meta and args.year is None:
        parser.error('Argument year  -y/--year is required to query the data')
    else:
        return vars(args)


def assign_constraints():
    """
    :return: kwargs: query arguments
    :return: outargs: output arguments
    """
    kwargs = parse_input()
    print(kwargs)
    # if print_meta option True print metadata definitions and exit
    if kwargs.pop('print_meta'):
        print_meta(wath_meta)
        sys.exit()
    #admin = kwargs.pop("admin")
    out_args, kwargs = output_args(kwargs)
    # build separate boolean arguments from meta option
    extra_args = meta_arguments(kwargs.pop("meta"), wath_meta)
    kwargs.update(extra_args)
    # if sst and year have only one value convert list to string
    for k in ['sst', 'year']:
        if len(kwargs[k]) == 1:
            kwargs[k] = kwargs[k][0]
        # copy remaining arguments and eliminate the ones which are empty or None
    for k, v in list(kwargs.items()):
        if v is None or v == []:
            kwargs.pop(k)
    return kwargs, out_args


def output_args(kwargs):
    """
     :param kwargs: input parameters
     :return: args: dictionary of arguments related to output format
     :return: kwargs: dictionary of remaining arguments relating to query
    """
    args = {'opendap': kwargs.pop("opendap"), 'ncss': kwargs.pop("ncss"), 'variable': kwargs.pop("variable"),
            'output_kind': kwargs.pop("output_kind"), 'download': kwargs.pop("download"),
            'download_path': kwargs.pop("download_path")}
    return args, kwargs


def build_query(kwargs):
    """
     :param kwargs: input arguments for query
     :return: string defining query
    """
    print(kwargs)
    query = '''asset.query :where "namespace>='/WatH-Test/model_output2/' and '''
    # define MF metadata namespace containing metadata documents
    namespace = "weather_at_home"
    for k, v in kwargs.items():
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
    return query[:-4] + '"'


# def build_action(out_args):
#    ''' build action to perform on results returned by query '''
#    opendap_urls = ''' :action get-distinct-values :xpath -ename url string.format('https://thredds.com.au%s?',''' +
#                   '''replace(xvalue('namespace'),'/WatH-Test/model_output2','')) '''
#    download_urls = ''' :action get-distinct-values :xpath -ename '''
#    count = ''' :action count '''


def process_output():
    """
    :return:
    """
    pass
    return


def main():
    """
     main program
    """
    global tds, xml_suf
    # parse input arguments 
    query_args, out_args = assign_constraints()
    print(out_args)
    # thredds root url
    tds = 'http://144.6.229.249/thredds/catalog/'
    html_suf = '/catalog.html'
    xml_suf = '/catalog.xml'
    ncss_suf = '/dataset.html'
    # establish session 
    session = MF.connect()
    # build query and then call MF.query to execute
    squery = build_query(query_args)
    # saction = ""
    # saction = 'count'
    saction = '''get-distinct-values :xpath -ename url''' + \
              ''' "replace(xvalue('namespace'),'/WatH-Test/model_output2/','')"'''
    output = session.query(squery, action=saction)
    # do something with result!
    #lname_dict = {'pcl': '/global_monthly_mean_diagnostic_',
    #              'pdl': '/regional_daily_mean_diagnostic_',
    #              'pel': '/regional_monthly_mean_diagnostic_'}
    if out_args['opendap'] or out_args['ncss']:
        tds_urls = []
        odap_urls = []
        ncss_urls = []
        if out_args['output_kind']:
            tds_tail = [ html_suf + "?dataset=WathA/#_" + x + ".ncml"
                         for x in out_args['output_kind']]
            odap_tail = ["/#_" + x + ".ncml.html" for x in out_args['output_kind']]
        else:
            tds_tail = [html_suf]
        # dataset = tds_connect()
        for path in session.response(output,saction):
            umid = path.split("/")[-1]
            root = tds + 'WatHA/' + path
            tds_urls.extend([ root + y.replace("#",path + "/" + umid) for y in tds_tail])
            odap_urls.extend([root.replace("catalog","dodsC") + y.replace("#",umid) for y in odap_tail])
            ncss_urls.extend([root.replace("catalog", "ncss") + y.replace("#", umid)[:-5] + ncss_suf for y in odap_tail])
            # http://144.6.229.249/thredds/dodsC/WatHA/2013/NAT/HadGEM2-ES/dir00001/n783/n783.pel.ncml.html
            # http://144.6.229.249/thredds/catalog/WatHA/2013/NAT/HadGEM2-ES/dir00001/n783/catalog.html?
            # dataset=WathA/2013/NAT/HadGEM2-ES/dir00001/n783/n783_pel.ncml
            # http://144.6.229.249/thredds/ncss/WatHA/2013/NAT/HadGEM2-ES/dir00001/n783/n783_pcl.ncml/dataset.html
    print(tds_urls)
    print(odap_urls)
    print(ncss_urls)
    # add subset ncss option if variables are passed and ncss is true and odap option if variables are passed and odap true
    print( ncss_subset(tds))

if __name__ == "__main__":
    main()
