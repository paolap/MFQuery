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

import pickle

# experiment_description metadata
wath_meta = { 'year': ['string', 'Name of W@h experiment', 'experiment_description'],
  'umid_range/min': ['string', 'Minimum of umid-range: range of possible umids associated to the experiment, '+
                     'alphabetical order is first ascii_lowercase then digits. ' +
                     'The umid of any simulations for a given experiment falls into this range', 'experiment_description'],
  'umid_range/max': ['string', 'Maximum of umid-range: range of possible umids associated to the experiment, ' +
                     'alphabetical order is first ascii_lowercase then digits. The umid of any simulations for a ' +
                     'given experiment falls into this range', 'experiment_description'],
 'runs_number': ['integer', 'number of simulations created for the experiment', 'experiment_description'],
 'created_on': ['string', 'Date when experiment simulations executables were created', 'experiment_description'],
 'restart_file': ['string', 'umid of restart file', 'experiment_description'],
 'batch': ['string', 'batch number followed by sub-batch if present', 'experiment_description'],
 'forcing': ['string', 'If experiment uses "all forcing" (all) or only natural forcing (NAT)', 'experiment_description'],
 'sst': ['string', 'Indicates if and how the sea surface temperature (SST) for that year obtained from ostia dataset' +
       'has been modified by subtracting a delta representing human contribution in natural forcing only simualtions.' +
       'If a delta has been added then list the general circulation model used to calculate it.', 'experiment_description'],
 'ozone': ['string', 'If ozone hole forcing has been used in the simulation: can be "all forcing ozone" or "NAT ozone"',
           'experiment_description'],
 'ENSO':  ['string', 'ElNino indicate if experiment is an El Nino , La Nina or Neutral year', 'experiment_description'],
 'ghg': ['boolean', 'If greenhouse gases (GHG) forcing is present or not', 'experiment_description'],
 'spin_up': ['boolean', 'If experiment is a suite of spin_up simulations', 'experiment_description'],
 'perturbed': ['boolean', 'If SST has been perturbed. For each SST-scenario there are about 6 thousands simulations ' +
               'each with a different perturbation of potential temperature in the atmosphere. The perturbations ' +
               'are generated as a random number using a small range of values.', 'experiment_description'],
 'wind_rh': ['boolean', 'If wind_rh is present', 'experiment_description'],
 'ffdi': ['boolean', 'If FFDI fire index is present', 'experiment_description'],
 'stash': ['boolean', 'If stash', 'experiment_description'],
 'xml_file': ['url', 'url pointing to a github repository of the xml_files containing the simulation code ' +
              'Ex. https://github.com/MitchellBlack/weatherathome/blob/4912c31057075e96720e5fd3abe9f8aba7488a5e/' +
              'xml_codes.dir/xml_anz.dir/archive.dir/wu_HadAM3P_ANZ_NIWA_n826_n9ei_MPI-ESM-P.xml', 'experiment_description'],
 'description': ['string', 'This collate all the textual descriptions and comments fields relating to the experiment',
                 'experiment_description'],
 'dynamics': ['string', 'Dynamics template used to set up simulations for experiment', 'experiment_description'],
 'experiment_id': ['integer', 'ID of experiment in original metadata database', 'experiment_description'],
 'creator': ['string', 'The person who generated the experiment', 'experiment_description'],
 'creator_email': ['email-address', 'e-mail of the experiment creator', 'experiment_description'],
# drs_meta metadata
 'umid': ['string', 'Model simulation id indicating the experiment. Umid are unique in one experiment context',
          'drs_meta'],
 'year': ['string', 'The year indicating the experiment, if 2012 then experiment simulations run from Dec 2012 to ' +
          'November 2013 included', 'drs_meta'],
 'volunteer': ['string', 'Unique volunteer id used in to name zip files containing a simulation output and in ' +
               'directory grouping them', 'drs_meta'] }
# save dictionary in pickle file
f=open("meta_doc_pickle","wb")
pickle.dump( wath_meta, f, protocol=2 )
f.close()
