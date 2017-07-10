import pytest
import sys

# Make session fixture available to doctests
#from tests.MF.MF import session

collect_ignore = ["setup.py", "docs/conf.py"]

# Pyesgf doesn't work with python 3
#if sys.version_info >= (3,0):
    #collect_ignore.append('WatHQuery/WatH/')
    #collect_ignore.append('WatHQuery/WatH/compare_helpers.py')
