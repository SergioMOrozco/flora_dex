import os
import numpy as np
import h5py
import random


def append_to_dataset(filename, data, dataset_name):
    hf = h5py.File(filename, "a")

    if dataset_name in hf.keys():

        hf[dataset_name].resize(hf[dataset_name].shape[0] + data.shape[0], axis=0)
        hf[dataset_name][-data.shape[0] :] = data

    else:

        hf.create_dataset(
            dataset_name,
            data=data,
            compression="gzip",
            chunks=True,
            maxshape=tuple([None] + list(data.shape[1:])),
        )

    print("'{0}' chunk has shape:{1}".format(dataset_name, hf[dataset_name].shape))

    hf.close()


def shuffle_dataset(filename, dataset_name, seed=None):

    i = 0
    batches = 500
    shuffled_data = []

    hf = h5py.File(filename, "a")

    hf["temp"] = hf[dataset_name]

    del hf[dataset_name]

    if not (seed == None):
        random.seed(seed)

    shuffled_indices = random.sample(range(hf["temp"].shape[0]), hf["temp"].shape[0])

    for index in shuffled_indices:
        if i >= batches:
            append_to_dataset(filename, np.array(shuffled_data), dataset_name)
            shuffled_data = []
            i = 0

        shuffled_data.append(hf["temp"][index])

        i += 1

    if not (shuffled_data == []):
        append_to_dataset(filename, np.array(shuffled_data), dataset_name)
        shuffled_data = []

    del hf["temp"]

    hf.close()
