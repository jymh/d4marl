import h5py
import numpy as np

data_dict = {}

def get_keys(h5file):
    keys = []

    def visitor(name, item):
        if isinstance(item, h5py.Dataset):
            keys.append(name)

    h5file.visititems(visitor)
    return keys

with h5py.File('/home/lhmeng/Datasetproj/on-policy/offline_datasets/hdf5_files/3m_no_quality.hdf5', 'r') as dataset_file:
    '''
    for k in get_keys(dataset_file):
        try:
            data_dict[k] = dataset_file[k][:]
        except ValueError as e:
            continue
    '''
    print(np.array(dataset_file['terminals']).shape)
