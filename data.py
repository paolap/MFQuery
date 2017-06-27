import pickle

# load mip and frequency dictionaries
def _read_pickle():
    # Read the packaged data
    from pkg_resources import resource_stream
    pickle_stream = resource_stream(__name__, 'data/meta_doc_pickle')
    drs_meta = pickle.load(pickle_stream)
    experiment_meta = pickle.load(pickle_stream)
    return drs_meta, experiment_meta

drs_meta, experiment_meta = _read_pickle()
