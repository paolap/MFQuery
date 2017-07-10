import pickle

# load mip and frequency dictionaries
def _read_pickle():
    # Read the packaged data
    from pkg_resources import resource_stream
    pickle_stream = resource_stream(__name__, 'data/meta_doc_pickle')
    wath_meta = pickle.load(pickle_stream)
    return wath_meta

wath_meta = _read_pickle()
